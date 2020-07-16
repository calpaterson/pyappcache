from typing import Optional, Any
from logging import getLogger

from .cache import Cache

logger = getLogger(__name__)


class MemcacheCache(Cache):
    """An implementation of Cache for memcache."""

    def __init__(self, client):
        super().__init__()
        self._mc = client

    def get_raw(self, raw_key: str) -> Optional[Any]:
        return self._mc.get(raw_key)

    def set_raw(self, raw_key: str, value_bytes: bytes, ttl: int) -> None:
        # FIXME: check that keys don't include control characters or whitespace
        # Or add a note?
        self._mc.set(raw_key, value_bytes, time=ttl)

    def invalidate_raw(self, raw_key: str) -> None:
        self._mc.delete(raw_key)

    def clear(self) -> None:
        """Clear the cache.

        Warning: memcache doesn't have a way to list keys so this clears
        everything!"""
        logger.warning("flushing memcache!")
        self._mc.flush_all()
