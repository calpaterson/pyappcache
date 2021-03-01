from typing import Optional

from ..cache import Cache
from ..keys import SimpleStringKey

CacheControlKey = SimpleStringKey[bytes]


class CacheControlProxy:
    """A proxy to allow :class:`~pyappcache.cache.Cache` instances to be
    converted for the cachecontrol library's desired API.

    """

    def __init__(self, cache: Cache):
        """

        :parameter cache: An instances of :class:`~pyappcache.Cache` to proxy."""
        self.cache = cache

    def get(self, key_str: str) -> Optional[bytes]:
        key = CacheControlKey(key_str)
        return self.cache.get(key)

    def set(self, key_str: str, value: bytes) -> None:
        key = CacheControlKey(key_str)
        self.cache.set(key, value)

    def delete(self, key_str: str) -> None:
        key = CacheControlKey(key_str)
        self.cache.invalidate(key)
