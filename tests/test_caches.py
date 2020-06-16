from datetime import timedelta
import time

from pyappcache.memcache import MemcacheCache
from pyappcache.redis import RedisCache
from pyappcache.keys import SimpleKey

import pytest

from .utils import random_string


@pytest.fixture(scope="session", params=["redis", "memcache"])
def cache(request):
    """Cache object"""
    if request.param == "redis":
        return RedisCache()
    else:
        return MemcacheCache()


def test_get_and_set_no_ttl(cache):
    key = SimpleKey(random_string())
    cache.set(key, 1)
    assert cache.get(key) == 1


def test_get_and_set_1_sec_ttl(cache):
    key = SimpleKey(random_string())
    if isinstance(cache, MemcacheCache):
        # FIXME: Check out of band, via stats
        cache.set(key, 1, ttl_seconds=1)
        assert cache.get(key) == 1
        time.sleep(1)
        assert cache.get(key) is None
    else:
        cache.set(key, 1, ttl_seconds=10_000)
        assert cache.get(key) == 1
        assert cache._redis.ttl(b"".join(key.as_bytes())) > 9_000


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
