from io import BytesIO

from pyappcache.cache import Cache
from pyappcache.keys import build_raw_key
from pyappcache.memcache import MemcacheCache
from pyappcache.sqlite_lru import SqliteCache
from pyappcache.redis import RedisCache
from pyappcache.fs import FilesystemCache

import pytest
from .utils import random_string, StringToStringKeyWithCompression, random_bytes


def test_get_and_set_no_ttl(cache, KeyCls):
    v = "a"
    key = KeyCls(random_string())
    cache.set(key, v)
    got = cache.get(key)
    assert got == v


def test_ttl_when_key_not_set(cache):
    if not hasattr(cache, "ttl"):
        pytest.skip("ttl is not implemented")
    key = random_string().encode("utf-8")
    assert cache.ttl(key) is None


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
    elif isinstance(cache, FilesystemCache):
        ttl = cache.ttl(key_str)
    elif isinstance(cache, RedisCache):
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
    key_segments = [cache.prefix]
    key_segments.extend(key.cache_key_segments())
    key_bytes = "/".join(key_segments)
    cache.set_raw(key_bytes, BytesIO(b"good luck unpickling this"), 0)

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

    cache.invalidate_by_str(str_key)
    assert cache.get_by_str(key) is None

    cache.set_by_str(str_key, "b")
    assert cache.get(key) == "b"

    cache.invalidate_by_str(str_key)
    assert cache.get(key) is None


def test_compression_via_key(cache):
    key = StringToStringKeyWithCompression(random_string())
    cache.set(key, "b")

    raw_value = cache.get_raw(build_raw_key(cache.prefix, key)).read()
    assert raw_value.startswith(b"\x1f\x8b")


def test_compression_via_str(cache):
    cache.set_by_str("a", "b", compress=True)
    raw_value = cache.get_raw(build_raw_key(cache.prefix, "a")).read()
    assert raw_value.startswith(b"\x1f\x8b")


def test_get_via(cache, KeyCls):
    key = KeyCls(random_string())

    getter_called = False

    def fake_getter():
        nonlocal getter_called
        getter_called = True
        return "ok"

    cache.get_via(key, fake_getter)
    assert getter_called is True

    getter_called = False
    cache.get_via(key, fake_getter)
    assert getter_called is False


def test_set_via(cache, KeyCls):
    key = KeyCls(random_string())

    db = {}

    def fake_setter(id_, value):
        db[id_] = value

    value = random_string()
    cache.set_via(key, value, fake_setter, setter_args=("a", value))

    assert cache.get(key) == value
    assert db["a"] == value


def test_set_via_setter_fails(cache, KeyCls):
    key = KeyCls(random_string())

    def fake_setter(id_, value):
        raise RuntimeError("bad bytes!")

    value = random_string()
    with pytest.raises(RuntimeError):
        cache.set_via(key, value, fake_setter, setter_args=("a", value))

    assert cache.get(key) is None


def test_default_prefix(cache):
    cache.prefix = Cache.DEFAULT_PREFIX
    key = random_string()
    value = random_string()
    cache.set_by_str(key, value)

    assert cache.get_raw("/".join(["pyappcache", key])) is not None


def test_eviction__max_size_is_maintained(cache):
    """Test that eviction happens on set_raw."""
    if not hasattr(cache, "max_size_bytes"):
        pytest.skip(reason="cache doesn't have a max_size_bytes param")

    cache.max_size_bytes = 100

    a_val = random_bytes(49)
    b_val = random_bytes(49)
    c_val = random_bytes(49)

    cache.set_raw("a", BytesIO(a_val), 100)
    cache.set_raw("b", BytesIO(b_val), 100)
    cache.set_raw("c", BytesIO(c_val), 100)

    assert cache.get_raw("a") is None
    assert cache.get_raw("b").read() == b_val
    assert cache.get_raw("c").read() == c_val


def test_eviction__reading_is_a_touch(cache):
    if not hasattr(cache, "max_size_bytes"):
        pytest.skip(reason="cache doesn't have a max_size_bytes param")

    cache.max_size_bytes = 100

    a_val = random_bytes(49)
    b_val = random_bytes(49)
    c_val = random_bytes(49)

    cache.set_raw("a", BytesIO(a_val), 100)
    cache.set_raw("b", BytesIO(b_val), 100)
    cache.get_raw("a")
    cache.set_raw("c", BytesIO(c_val), 100)

    assert cache.get_raw("a").read() == a_val
    assert cache.get_raw("b") is None
    assert cache.get_raw("c").read() == c_val
