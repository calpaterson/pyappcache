from typing import Optional, cast
from logging import getLogger

import redis as redis_py

from .cache import Cache

logger = getLogger(__name__)


class RedisCache(Cache):
    """An implementation of Cache for memcache."""

    def __init__(self, client: redis_py.Redis):
        super().__init__()
        self._redis = client

    def get_raw(self, raw_key: str) -> Optional[bytes]:
        return cast(Optional[bytes], self._redis.get(raw_key))

    def set_raw(self, raw_key: str, value_bytes: bytes, ttl_seconds: int) -> None:
        self._redis.set(
            raw_key, value_bytes, ex=ttl_seconds if ttl_seconds != 0 else None
        )

    def invalidate_raw(self, raw_key: str) -> None:
        self._redis.delete(raw_key)

    def clear(self) -> None:
        self._redis.flushdb()
