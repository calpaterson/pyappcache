import pylibmc

from typing import Optional, Any
from logging import getLogger

from .cache import Cache

logger = getLogger(__name__)


class MemcacheCache(Cache):
    """An implementation of Cache for memcache.

    All methods in this class will retry exactly once when the underlying
    pylibmc client returns a ConnectionError (to be robust against memcache
    restarts.
    """

    def __init__(self, client):
        """

        :param client: A (pylibmc) memcache client to use."""
        super().__init__()
        self._mc = client

    def get_raw(self, raw_key: str) -> Optional[Any]:
        try:
            return self._mc.get(raw_key)
        except pylibmc.ConnectionError:
            logger.warning("got a connection error from pylibmc, retrying once")
        return self._mc.get(raw_key)

    def set_raw(self, raw_key: str, value_bytes: bytes, ttl: int) -> None:
        # FIXME: check that keys don't include control characters or whitespace
        # Or add a note?
        try:
            self._mc.set(raw_key, value_bytes, time=ttl)
        except pylibmc.ConnectionError:
            logger.warning("got a connection error from pylibmc, retrying once")
        self._mc.set(raw_key, value_bytes, time=ttl)

    def invalidate_raw(self, raw_key: str) -> None:
        try:
            self._mc.delete(raw_key)
        except pylibmc.ConnectionError:
            logger.warning("got a connection error from pylibmc, retrying once")
        self._mc.delete(raw_key)

    def clear(self) -> None:
        """Clear the cache.

        Warning: memcache doesn't have a way to list keys so this clears
        everything!"""
        logger.warning("flushing memcache!")
        try:
            self._mc.flush_all()
        except pylibmc.ConnectionError:
            logger.warning("got a connection error from pylibmc, retrying once")
            self._mc.flush_all()
