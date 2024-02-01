import threading
from datetime import datetime, timedelta
from contextlib import closing
import socket
import time

import requests
import cachecontrol
import flask

import requests.models
import requests.adapters
import pytest

from pyappcache.util.requests import CacheControlProxy


def get_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def local_server():
    app = flask.Flask("local-server")
    app.config["calls"] = 0

    @app.route("/", methods=["GET"])
    def get_route():
        response = flask.make_response(b"hello")
        response.headers["Cache-Control"] = "max-age=200"
        app.config["calls"] += 1
        return response

    @app.route("/ok", methods=["GET"])
    def ok():
        return "ok"

    @app.route("/", methods=["DELETE"])
    def delete_route():
        response = flask.make_response(b"goodbye")
        app.config["calls"] += 1
        return response

    port = get_free_port()

    thread = threading.Thread(
        target=app.run, kwargs={"port": port, "debug": False}, daemon=True
    )
    thread.start()

    # Wait until the server has started up (check by polling)
    give_up_time = datetime.utcnow() + timedelta(seconds=5)
    sesh = requests.Session()
    while give_up_time > datetime.utcnow():
        try:
            sesh.get(f"http://localhost:{port}/ok", timeout=0.001)
            break
        except requests.exceptions.RequestException:
            pass
        time.sleep(0)  # aka thread.yield

    return app, port


def test_request_with_cache_control(cache, local_server):
    """Check that requests are cached properly"""
    app, port = local_server
    initial_calls = app.config["calls"]

    url = f"http://localhost:{port}/"

    proxy = CacheControlProxy(cache)

    sesh = requests.Session()
    cached_sesh = cachecontrol.CacheControl(sesh, cache=proxy)  # type: ignore

    response1 = cached_sesh.get(url)
    assert response1.status_code == 200
    assert response1.content == b"hello"

    response2 = cached_sesh.get(url)
    assert response2.status_code == 200
    assert response2.content == b"hello"

    assert app.config["calls"] == (initial_calls + 1)


def test_deletion_with_cache_control(cache, local_server):
    """Check that issuing a delete clears the entry from the cache"""
    app, port = local_server

    url = f"http://localhost:{port}/"

    proxy = CacheControlProxy(cache)

    sesh = requests.Session()
    cached_sesh = cachecontrol.CacheControl(sesh, cache=proxy)  # type: ignore

    response1 = cached_sesh.get(url)
    assert response1.status_code == 200
    assert response1.content == b"hello"

    response2 = cached_sesh.delete(url)
    assert response2.status_code == 200
    assert response2.content == b"goodbye"

    assert proxy.get(url) is None
