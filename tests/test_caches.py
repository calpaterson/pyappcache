from datetime import timedelta
import time

from pyappcache.memcache import MemcacheCache
from pyappcache.keys import SimpleKey

import pytest

from .utils import random_string


@pytest.fixture(scope="session")
def cache():
    """Cache object"""
    return MemcacheCache()


def test_get_and_set_no_ttl(cache):
    key = SimpleKey(random_string())
    cache.set(key, 1)
    assert cache.get(key) == 1


def test_get_and_set_1_sec_ttl(cache):
    key = SimpleKey(random_string())
    cache.set(key, 1, ttl_seconds=1)
    assert cache.get(key) == 1

    # for memcache, no easy way to check ttl
    time.sleep(1)
    assert cache.get(key) is None


def test_get_and_set_absent(cache):
    key = SimpleKey(random_string())
    assert cache.get(key) is None


def test_invalidate(cache):
    key = SimpleKey(random_string())
    cache.set(key, 1)
    cache.invalidate(key)
    assert cache.get(key) is None


def test_clear(cache):
    key = SimpleKey(random_string())
    cache.set(key, 1)
    cache.clear()
    assert cache.get(key) is None


def test_unreadable_pickle(cache):
    key = SimpleKey(random_string())
    key_bytes = b"".join(key.as_bytes())
    cache.set_raw(key_bytes, b"good luck unpickling this", 0)

    assert cache.get(key) is None
