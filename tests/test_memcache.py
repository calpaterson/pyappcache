import pickle
import pylibmc

import pytest

from pyappcache.memcache import MemcacheCache
from .utils import random_string


class FlakeyClient:
    def __init__(self, flakes):
        self.count = 0
        self.flakes = flakes

    def get(self, key):
        if self.count >= self.flakes:
            return pickle.dumps("good bytes")
        else:
            self.count += 1
            raise pylibmc.ConnectionError("nope")

    def set(self, key, value, time):
        if self.count >= self.flakes:
            return None
        else:
            self.count += 1
            raise pylibmc.ConnectionError("nope")

    def delete(self, key):
        if self.count >= self.flakes:
            return None
        else:
            self.count += 1
            raise pylibmc.ConnectionError("nope")

    def flush_all(self):
        if self.count >= self.flakes:
            return None
        else:
            self.count += 1
            raise pylibmc.ConnectionError("nope")


@pytest.mark.parametrize(
    "method_name, args, expected",
    [
        ("get_by_str", ("a",), "good bytes"),
        ("set_by_str", ("a", "b"), None),
        ("invalidate_by_str", ("a"), None),
        ("clear", (), None),
    ],
)
def test_retry_on_disconnect(method_name, args, expected):
    """Check we try to reconnect (exactly once) to the memcache server if we get disconnected."""

    cache = MemcacheCache(FlakeyClient(1))
    assert getattr(cache, method_name)(*args) == expected


def test_retry_gives_up_on_down():
    """Check we don't retry forever"""

    cache = MemcacheCache(FlakeyClient(2))
    with pytest.raises(pylibmc.ConnectionError):
        cache.get_by_str("foo")


def test_default_client():
    cache = MemcacheCache()
    cache.get_by_str(random_string()) is None
