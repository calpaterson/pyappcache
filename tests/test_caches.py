from pyappcache.memcache import MemcacheCache
from pyappcache.keys import SimpleKey

import pytest

from .utils import random_string


@pytest.fixture(scope="session")
def cache():
    """Cache object"""
    return MemcacheCache()


def test_get_and_set(cache):
    key = SimpleKey(random_string())
    cache.set(key, 1)
    assert cache.get(key) == 1

    # TODO: Check TTL
