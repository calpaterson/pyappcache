from typing import Sequence, Mapping, Optional
from logging import getLogger

import pylibmc

from .keys import Key
from .cache import Cache, K_inv, V_inv
from .serialisation import PickleSerialiser

logger = getLogger(__name__)


class MemcacheCache(Cache):
    """An implementation of Cache for memcache."""

    def __init__(
        self,
        client_args: Optional[Sequence] = None,
        client_kwargs: Optional[Mapping] = None,
    ):
        if client_args is None:
            client_args = [["127.0.0.1"]]
        if client_kwargs is None:
            client_kwargs = {}

        self._mc = pylibmc.Client(*client_args, **client_kwargs)
        self.serialiser = PickleSerialiser()
        logger.debug("connected to %s", client_args[0])

    def get(self, key: Key[K_inv, V_inv]) -> Optional[V_inv]:
        cache_contents = self._mc.get(b"".join(key.as_bytes()))
        if cache_contents is not None:
            return self.serialiser.loads(cache_contents)
        else:
            return None

    def set(self, key: Key[K_inv, V_inv], value: V_inv, ttl_seconds: int = 0) -> None:
        self.set_raw(
            b"".join(key.as_bytes()), self.serialiser.dumps(value), ttl_seconds
        )

    def set_raw(self, key_bytes: bytes, value_bytes: bytes, ttl: int) -> None:
        self._mc.set(key_bytes, value_bytes, time=ttl)

    def invalidate(self, key: Key[K_inv, V_inv]) -> None:
        self._mc.delete(b"".join(key.as_bytes()))

    def clear(self) -> None:
        """Clear the cache.

        Warning: memcache doesn't have a way to list keys so this clears
        everything!"""
        logger.warning("flushing memcache!")
        self._mc.flush_all()
