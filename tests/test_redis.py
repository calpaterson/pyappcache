from pyappcache.redis import RedisCache
from .utils import random_string


def test_default_client():
    cache = RedisCache()
    cache.get_by_str(random_string()) is None
