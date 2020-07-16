import redis as redis_py
import pylibmc

from pyappcache.cache import Cache
from pyappcache.memcache import MemcacheCache
from pyappcache.redis import RedisCache
from pyappcache.sqlite_lru import SqliteCache

import pytest
from .utils import random_string, StringToStringKey, StringToStringKeyWithCompression


@pytest.fixture(scope="session")
def memcache_client():
    return pylibmc.Client(["127.0.0.1"], binary=True)


@pytest.fixture(scope="session")
def redis_client():
    return redis_py.Redis()


@pytest.fixture(scope="function", params=["redis", "memcache", "sqlite"])
def cache(request, redis_client, memcache_client):
    """Cache object"""
    cache: Cache
    if request.param == "redis":
        cache = RedisCache(redis_client)
    elif request.param == "sqlite":
        cache = SqliteCache()
    else:
        cache = MemcacheCache(memcache_client)

    # Randomise the prefix
    cache.prefix = random_string()

    return cache


@pytest.fixture(params=[StringToStringKey, StringToStringKeyWithCompression])
def KeyCls(request):
    return request.param
