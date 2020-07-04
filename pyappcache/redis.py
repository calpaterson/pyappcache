from typing import Sequence, Mapping, Optional
from logging import getLogger

import redis as redis_py

from .keys import Key, build_raw_key
from .cache import Cache, V_inv
from .serialisation import PickleSerialiser

logger = getLogger(__name__)


class RedisCache(Cache):
    """An implementation of Cache for memcache."""

    def __init__(
        self,
        client_args: Optional[Sequence] = None,
        client_kwargs: Optional[Mapping] = None,
    ):
        self.serialiser = PickleSerialiser()
        if client_args is None:
            client_args = []
        if client_kwargs is None:
            client_kwargs = {}

        self._redis = redis_py.Redis(*client_args, **client_kwargs)
        logger.debug("connected to %s", self._redis.connection_pool.connection_kwargs)

    def get(self, key: Key[V_inv]) -> Optional[V_inv]:
        cache_contents = self._redis.get(build_raw_key(self.prefix, key))
        if cache_contents is not None:
            return self.serialiser.loads(cache_contents)
        else:
            return None

    def set(self, key: Key[V_inv], value: V_inv, ttl_seconds: int = 0) -> None:
        self.set_raw(
            build_raw_key(self.prefix, key), self.serialiser.dumps(value), ttl_seconds
        )

    def set_raw(self, key_bytes: bytes, value_bytes: bytes, ttl: int) -> None:
        self._redis.set(key_bytes, value_bytes, ex=ttl if ttl != 0 else None)

    def invalidate(self, key: Key) -> None:
        self._redis.delete(build_raw_key(self.prefix, key))

    def clear(self) -> None:
        self._redis.flushdb()
