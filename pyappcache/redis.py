import io
from typing import Optional, cast, IO
from logging import getLogger

import redis as redis_py

from .cache import Cache

logger = getLogger(__name__)


class RedisCache(Cache):
    """A redis :class:`~pyappcache.cache.Cache` instance.

    This uses ``GET``/``SET``/``DELETE``.

    .. admonition:: :meth:`~Cache.clear` uses ``FLUSHDB``

       The clear method for this implementation will call ``FLUSHDB`` - and so
       remove *everything* in the database.

    """

    def __init__(self, client: Optional[redis_py.Redis] = None):
        """

        :param client: A optional redis client to use.  If one isn't provided
            database 0 on localhost is used."""
        super().__init__()
        if client is not None:
            self._redis = client
        else:
            self._redis = redis_py.Redis()

    def get_raw(self, raw_key: str) -> Optional[IO[bytes]]:
        value = self._redis.get(raw_key)
        if value is not None:
            return io.BytesIO(cast(bytes, value))
        else:
            return None

    def set_raw(self, raw_key: str, value_bytes: IO[bytes], ttl_seconds: int) -> None:
        self._redis.set(
            raw_key, value_bytes.read(), ex=ttl_seconds if ttl_seconds != 0 else None
        )

    def invalidate_raw(self, raw_key: str) -> None:
        self._redis.delete(raw_key)

    def clear(self) -> None:
        self._redis.flushdb()
