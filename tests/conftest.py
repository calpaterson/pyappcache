from pathlib import Path

import redis as redis_py
import pylibmc

from pyappcache.cache import Cache
from pyappcache.memcache import MemcacheCache
from pyappcache.redis import RedisCache
from pyappcache.sqlite_lru import SqliteCache
from pyappcache.fs import FilesystemCache

import pytest
from .utils import random_string, StringToStringKey, StringToStringKeyWithCompression


@pytest.fixture(scope="session")
def memcache_client():
    return pylibmc.Client(["127.0.0.1"], binary=True)


@pytest.fixture(scope="session")
def redis_client():
    return redis_py.Redis()


@pytest.fixture(scope="function", params=["redis", "memcache", "sqlite", "fs"])
def cache(request, redis_client, memcache_client, tmpdir):
    """Cache object"""
    cache: Cache
    if request.param == "redis":
        cache = RedisCache(redis_client)
    elif request.param == "sqlite":
        cache = SqliteCache()
    elif request.param == "fs":
        cache = FilesystemCache(Path(str(tmpdir)))
    else:
        cache = MemcacheCache(memcache_client)

    # Randomise the prefix
    cache.prefix = random_string()

    return cache


@pytest.fixture(params=[StringToStringKey, StringToStringKeyWithCompression])
def KeyCls(request):
    return request.param


test_data = Path(__file__).parent.resolve() / "test-data"
