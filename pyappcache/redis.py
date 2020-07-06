from typing import Optional, Any
from logging import getLogger

import redis as redis_py

from .keys import Key, build_raw_key
from .cache import Cache, V_inv

logger = getLogger(__name__)


class RedisCache(Cache):
    """An implementation of Cache for memcache."""

    def __init__(self, client: redis_py.Redis):
        super().__init__()
        self._redis = client

    def get(self, key: Key[V_inv]) -> Optional[V_inv]:
        return self.get_raw(build_raw_key(self.prefix, key))

    def get_by_str(self, key_str: str) -> Optional[Any]:
        return self.get_raw(build_raw_key(self.prefix, key_str))

    def get_raw(self, raw_key: str) -> Optional[Any]:
        cache_contents = self._redis.get(raw_key)
        if cache_contents is not None:
            return self.serialiser.loads(cache_contents)
        else:
            return None

    def set(self, key: Key[V_inv], value: V_inv, ttl_seconds: int = 0) -> None:
        self.set_raw(
            build_raw_key(self.prefix, key), self.serialiser.dumps(value), ttl_seconds
        )

    def set_by_str(self, key_str: str, value: V_inv, ttl_seconds: int = 0) -> None:
        self.set_raw(
            build_raw_key(self.prefix, key_str),
            self.serialiser.dumps(value),
            ttl_seconds,
        )

    def set_raw(self, key_bytes: str, value_bytes: bytes, ttl_seconds: int) -> None:
        self._redis.set(
            key_bytes, value_bytes, ex=ttl_seconds if ttl_seconds != 0 else None
        )

    def invalidate(self, key: Key) -> None:
        self._redis.delete(build_raw_key(self.prefix, key))

    def invalidate_by_str(self, key_str: str) -> None:
        self._redis.delete(build_raw_key(self.prefix, key_str))

    def clear(self) -> None:
        self._redis.flushdb()
