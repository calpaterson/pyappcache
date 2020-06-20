from typing import Type

from pyappcache.memcache import MemcacheCache
from pyappcache.redis import RedisCache
from pyappcache.keys import SimpleKey, Key
from pyappcache.cache import Cache

import pytest

from .utils import random_string, get_memcache_ttl


@pytest.fixture(scope="session", params=["redis", "memcache"])
def cache(request):
    """Cache object"""
    if request.param == "redis":
        return RedisCache()
    else:
        return MemcacheCache()
