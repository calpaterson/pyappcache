from typing import Optional, Any
from logging import getLogger

from .keys import Key, build_raw_key
from .cache import Cache, V_inv

logger = getLogger(__name__)


class MemcacheCache(Cache):
    """An implementation of Cache for memcache."""

    def __init__(self, client):
        super().__init__()
        self._mc = client

    def get_raw(self, raw_key: str) -> Optional[Any]:
        return self._mc.get(raw_key)

    def set_raw(self, key_str: str, value_bytes: bytes, ttl: int) -> None:
        self._mc.set(key_str, value_bytes, time=ttl)

    def invalidate(self, key: Key[V_inv]) -> None:
        self._mc.delete(build_raw_key(self.prefix, key))

    def invalidate_by_str(self, key_str: str) -> None:
        self._mc.delete(build_raw_key(self.prefix, key_str))

    def clear(self) -> None:
        """Clear the cache.

        Warning: memcache doesn't have a way to list keys so this clears
        everything!"""
        logger.warning("flushing memcache!")
        self._mc.flush_all()
