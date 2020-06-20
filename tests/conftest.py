from pyappcache.memcache import MemcacheCache
from pyappcache.redis import RedisCache

import pytest


@pytest.fixture(scope="session", params=["redis", "memcache"])
def cache(request):
    """Cache object"""
    if request.param == "redis":
        return RedisCache()
    else:
        return MemcacheCache()
