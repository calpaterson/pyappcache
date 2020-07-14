from typing import Optional, cast
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

    def get_raw(self, raw_key: str) -> Optional[bytes]:
        return cast(Optional[bytes], self._redis.get(raw_key))

    def set_raw(self, key_bytes: str, value_bytes: bytes, ttl_seconds: int) -> None:
        self._redis.set(
            key_bytes, value_bytes, ex=ttl_seconds if ttl_seconds != 0 else None
        )

    def invalidate(self, key: Key[V_inv]) -> None:
        self._redis.delete(build_raw_key(self.prefix, key))

    def invalidate_by_str(self, key_str: str) -> None:
        self._redis.delete(build_raw_key(self.prefix, key_str))

    def clear(self) -> None:
        self._redis.flushdb()
