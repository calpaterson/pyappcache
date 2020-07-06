from pyappcache.keys import build_raw_key
from pyappcache.memcache import MemcacheCache
from pyappcache.sqlite_lru import SqliteCache
from pyappcache.cache import Cache

import pytest
from .utils import random_string, StringToStringKey


class StringToStringKeyWithCompression(StringToStringKey):
    def should_compress(self, python_obj, as_bytes):
        return True


@pytest.fixture(params=[StringToStringKey, StringToStringKeyWithCompression])
def KeyCls(request):
    return request.param


def test_get_and_set_no_ttl(cache: Cache, KeyCls):
    v = "a"
    key = KeyCls(random_string())
    cache.set(key, v)
    got = cache.get(key)
    assert got == v


def test_get_and_set_10k_sec_ttl(cache, KeyCls):
    key = KeyCls(random_string())
    cache.set(key, "a", ttl_seconds=10_000)

    key_str = build_raw_key(cache.prefix, key)
    if isinstance(cache, MemcacheCache):
        # Is there any way to do this?
        pytest.skip("memcache ttl checker is too flaky")
        # ttl = get_memcache_ttl(key_str)
    elif isinstance(cache, SqliteCache):
        ttl = cache.ttl(key_str)
    else:
        ttl = cache._redis.ttl(key_str)
    assert cache.get(key) == "a"
    assert ttl is not None
    assert ttl > 9_000


def test_overwrite(cache, KeyCls):
    key = KeyCls(random_string())
    cache.set(key, "a")
    cache.set(key, "b")
    assert cache.get(key) == "b"


def test_get_and_set_absent(cache, KeyCls):
    key = KeyCls(random_string())
    assert cache.get(key) is None


def test_invalidate(cache, KeyCls):
    key = KeyCls(random_string())
    cache.set(key, "a")
    cache.invalidate(key)
    assert cache.get(key) is None


def test_clear(cache, KeyCls):
    key = KeyCls(random_string())
    cache.set(key, "a")
    cache.clear()
    assert cache.get(key) is None


def test_unreadable_pickle(cache, KeyCls):
    key = KeyCls(random_string())
    key_bytes = cache.prefix + "".join(key.as_segments())
    cache.set_raw(key_bytes, b"good luck unpickling this", 0)

    assert cache.get(key) is None


def test_prefixing(cache, KeyCls):
    key = KeyCls(random_string())
    cache.set(key, "a")
    cache.prefix = random_string()
    assert cache.get(key) is None


def test_by_str(cache, KeyCls):
    key_subj = random_string()
    key = KeyCls(key_subj)
    str_key = key_subj

    cache.set(key, "a")
    assert cache.get_by_str(str_key) == "a"

    cache.invalidate(str_key)
    assert cache.get_by_str(key) is None

    cache.set_by_str(str_key, "b")
    assert cache.get(key) == "b"

    cache.invalidate_by_str(str_key)
    assert cache.get(key) is None


@pytest.mark.xfail(reason="not implemented")
def test_compression(cache):
    key = StringToStringKeyWithCompression(random_string())
    cache.set(key, "b")

    raw_value = cache.get_raw(build_raw_key(cache.prefix, key))
    assert raw_value.startswith(b"\x1f\x8b")
