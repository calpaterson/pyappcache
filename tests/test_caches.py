from pyappcache.keys import build_raw_key
from pyappcache.memcache import MemcacheCache
from pyappcache.sqlite_lru import SqliteCache
from pyappcache.cache import Cache

from .utils import random_string, get_memcache_ttl, StringToIntKey


def test_get_and_set_no_ttl(cache: Cache):
    v = 1
    key = StringToIntKey(random_string())
    cache.set(key, v)
    got = cache.get(key)
    assert got == v


def test_get_and_set_10k_sec_ttl(cache):
    key = StringToIntKey(random_string())
    cache.set(key, 1, ttl_seconds=10_000)

    key_str = build_raw_key(cache.prefix, key)
    if isinstance(cache, MemcacheCache):
        ttl = get_memcache_ttl(key_str)
    elif isinstance(cache, SqliteCache):
        ttl = cache.ttl(key_str)
    else:
        ttl = cache._redis.ttl(key_str)
    assert cache.get(key) == 1
    assert ttl is not None
    assert ttl > 9_000


def test_overwrite(cache):
    key = StringToIntKey(random_string())
    cache.set(key, 1)
    cache.set(key, 2)
    assert cache.get(key) == 2


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
    key_bytes = cache.prefix + "".join(key.as_segments())
    cache.set_raw(key_bytes, b"good luck unpickling this", 0)

    assert cache.get(key) is None


def test_prefixing(cache):
    key = StringToIntKey(random_string())
    cache.set(key, 0)
    cache.prefix = random_string()
    assert cache.get(key) is None


def test_by_str(cache):
    key_subj = random_string()
    key = StringToIntKey(key_subj)
    str_key = key_subj

    cache.set(key, 0)
    assert cache.get_by_str(str_key) == 0

    cache.invalidate(str_key)
    assert cache.get_by_str(key) is None

    cache.set_by_str(str_key, 1)
    assert cache.get(key) == 1

    cache.invalidate_by_str(str_key)
    assert cache.get(key) is None
