from pyappcache.memcache import MemcacheCache
from pyappcache.redis import RedisCache
from pyappcache.sqlite import SqliteCache

import pytest
from .utils import random_bytes


@pytest.fixture(scope="session", params=["redis", "memcache", "sqlite"])
def cache_instance(request):
    """Cache object"""
    if request.param == "redis":
        return RedisCache()
    elif request.param == "sqlite":
        return SqliteCache()
    else:
        return MemcacheCache()


@pytest.fixture(scope="function")
def cache(cache_instance):
    cache_instance.prefix = b"".join([b"/", random_bytes(), b"/"])
    return cache_instance
