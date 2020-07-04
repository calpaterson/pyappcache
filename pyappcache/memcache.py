from typing import Optional, Any
from logging import getLogger

from .keys import Key, build_raw_key
from .cache import Cache, V_inv
from .serialisation import PickleSerialiser

logger = getLogger(__name__)


class MemcacheCache(Cache):
    """An implementation of Cache for memcache."""

    def __init__(self, client):
        self._mc = client
        self.serialiser = PickleSerialiser()

    def get(self, key: Key[V_inv]) -> Optional[V_inv]:
        return self.get_raw(build_raw_key(self.prefix, key))

    def get_by_str(self, key_str: str) -> Any:
        return self.get_raw(build_raw_key(self.prefix, key_str))

    def get_raw(self, raw_key: str) -> Optional[Any]:
        cache_contents = self._mc.get(raw_key)
        if cache_contents is not None:
            return self.serialiser.loads(cache_contents)
        else:
            return None

    def set(self, key: Key[V_inv], value: V_inv, ttl_seconds: int = 0) -> None:
        self.set_raw(
            build_raw_key(self.prefix, key), self.serialiser.dumps(value), ttl_seconds
        )

    def set_by_str(self, key: str, value: V_inv, ttl_seconds: int = 0) -> None:
        self.set_raw(
            build_raw_key(self.prefix, key), self.serialiser.dumps(value), ttl_seconds
        )

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
