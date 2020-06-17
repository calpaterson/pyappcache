from typing import Type

from pyappcache.memcache import MemcacheCache
from pyappcache.redis import RedisCache
from pyappcache.keys import SimpleKey, Key
from pyappcache.cache import Cache

import pytest

from .utils import random_string, get_memcache_ttl


StringToIntKey: Type[Key[str, int]] = SimpleKey


@pytest.fixture(scope="session", params=["redis", "memcache"])
def cache(request):
    """Cache object"""
    if request.param == "redis":
        return RedisCache()
    else:
        return MemcacheCache()


def test_get_and_set_no_ttl(cache: Cache):
    v = 1
    key = StringToIntKey(random_string())
    cache.set(key, v)
    got = cache.get(key)
    assert got == v


def test_get_and_set_1_sec_ttl(cache):
    key = StringToIntKey(random_string())
    cache.set(key, 1, ttl_seconds=10_000)
    if isinstance(cache, MemcacheCache):
        ttl = get_memcache_ttl(b"".join(key.as_bytes()))
    else:
        ttl = cache._redis.ttl(b"".join(key.as_bytes()))
    assert cache.get(key) == 1
    assert ttl is not None
    assert ttl > 9_000


def test_get_and_set_absent(cache):
    key = StringToIntKey(random_string())
    assert cache.get(key) is None


def test_invalidate(cache):
    key = StringToIntKey(random_string())
    cache.set(key, 1)
    cache.invalidate(key)
    assert cache.get(key) is None


def test_clear(cache):
    key = StringToIntKey(random_string())
    cache.set(key, 1)
    cache.clear()
    assert cache.get(key) is None


def test_unreadable_pickle(cache):
    key = StringToIntKey(random_string())
    key_bytes = b"".join(key.as_bytes())
    cache.set_raw(key_bytes, b"good luck unpickling this", 0)

    assert cache.get(key) is None
