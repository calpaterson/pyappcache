from typing import Sequence, Mapping, Optional
import pickle
from logging import getLogger

import redis as redis_py

from .keys import Key
from .cache import Cache, S_inv

logger = getLogger(__name__)


class RedisCache(Cache):
    """An implementation of Cache for memcache."""

    def __init__(
        self,
        client_args: Optional[Sequence] = None,
        client_kwargs: Optional[Mapping] = None,
    ):
        if client_args is None:
            client_args = []
        if client_kwargs is None:
            client_kwargs = {}

        self._redis = redis_py.Redis(*client_args, **client_kwargs)
        logger.debug("connected to %s", self._redis.connection_pool.connection_kwargs)

    def get(self, key: Key[S_inv]) -> Optional[S_inv]:
        cache_contents = self._redis.get(b"".join(key.as_bytes()))
        if cache_contents is not None:
            try:
                value = pickle.loads(cache_contents)
            except pickle.UnpicklingError:
                value = None
            return value
        else:
            return None

    def set(self, key: Key[S_inv], value: S_inv, ttl_seconds: int = 0) -> None:
        self.set_raw(b"".join(key.as_bytes()), pickle.dumps(value), ttl_seconds)

    def set_raw(self, key_bytes: bytes, value_bytes: bytes, ttl: int) -> None:
        self._redis.set(key_bytes, value_bytes, ex=ttl if ttl != 0 else None)

    def invalidate(self, key: Key) -> None:
        self._redis.delete(b"".join(key.as_bytes()))

    def clear(self) -> None:
        self._redis.flushdb()
