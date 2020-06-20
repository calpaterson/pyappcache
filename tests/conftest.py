from pyappcache.memcache import MemcacheCache
from pyappcache.redis import RedisCache
from pyappcache.sqlite import SqliteCache

import pytest


@pytest.fixture(scope="session", params=["redis", "memcache", "sqlite"])
def cache(request):
    """Cache object"""
    if request.param == "redis":
        return RedisCache()
    elif request.param == "sqlite":
        return SqliteCache()
    else:
        return MemcacheCache()
