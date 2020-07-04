import redis as redis_py
import pylibmc

from pyappcache.memcache import MemcacheCache
from pyappcache.redis import RedisCache
from pyappcache.sqlite import SqliteCache

import pytest
from .utils import random_string


@pytest.fixture(scope="session", params=["redis", "memcache", "sqlite"])
def cache_instance(request):
    """Cache object"""
    if request.param == "redis":
        return RedisCache(redis_py.Redis())
    elif request.param == "sqlite":
        return SqliteCache()
    else:
        return MemcacheCache(pylibmc.Client(["127.0.0.1"]))


@pytest.fixture(scope="function")
def cache(cache_instance):
    cache_instance.prefix = "".join(["/", random_string(), "/"])
    return cache_instance
