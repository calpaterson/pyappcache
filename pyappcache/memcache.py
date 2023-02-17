import pylibmc
import io

from typing import Optional, Any, IO
from logging import getLogger

from .cache import Cache

logger = getLogger(__name__)


class MemcacheCache(Cache):
    """An implementation of Cache for memcache.

    All methods in this class will retry exactly once when the underlying
    pylibmc client returns a ConnectionError (to be robust against memcache
    restarts.
    """

    def __init__(self, client: Optional[Any] = None):
        """

        :param client: A optional (pylibmc-compatible) memcache client to use."""
        super().__init__()
        if client is not None:
            self._mc = client
        else:
            self._mc = pylibmc.Client(["127.0.0.1"], binary=True)

    def get_raw(self, raw_key: str) -> Optional[IO[bytes]]:
        try:
            value = self._mc.get(raw_key)
        except pylibmc.ConnectionError:
            logger.warning("got a connection error from pylibmc, retrying once")
            value = self._mc.get(raw_key)
        if value is not None:
            return io.BytesIO(value)
        else:
            return None

    def set_raw(self, raw_key: str, value_bytes: IO[bytes], ttl: int) -> None:
        # FIXME: check that keys don't include control characters or whitespace
        # Or add a note?
        try:
            self._mc.set(raw_key, value_bytes.read(), time=ttl)
            return
        except pylibmc.ConnectionError:
            logger.warning("got a connection error from pylibmc, retrying once")
        value_bytes.seek(0)
        self._mc.set(raw_key, value_bytes.read(), time=ttl)

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
