from typing import Sequence, Mapping, Optional, Any
import pickle
from logging import getLogger

import pylibmc

from .keys import Key
from .cache import Cache, S_inv

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
        logger.debug("connected to %s", client_args[0])

    def get(self, key: Key[S_inv]) -> Optional[S_inv]:
        cache_contents = self._mc.get(b"".join(key.as_bytes()))
        if cache_contents is not None:
            try:
                value = pickle.loads(cache_contents)
            except pickle.UnpicklingError:
                logger.warning("unable to unpickle value for %s", key)
                value = None
            return value
        else:
            return None

    def set(self, key: Key[S_inv], value: S_inv, ttl_seconds: int = 0) -> None:
        self.set_raw(b"".join(key.as_bytes()), pickle.dumps(value), ttl_seconds)

    def set_raw(self, key_bytes: bytes, value_bytes: bytes, ttl: int) -> None:
        self._mc.set(key_bytes, value_bytes, time=ttl)

    def invalidate(self, key: Key[S_inv]) -> None:
        self._mc.delete(b"".join(key.as_bytes()))

    def clear(self) -> None:
        """Clear the cache.

        Warning: memcache doesn't have a way to list keys so this clears
        everything!"""
        logger.warning("flushing memcache!")
        self._mc.flush_all()
