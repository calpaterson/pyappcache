from datetime import timedelta
from typing import Sequence, Mapping, Optional, Any
import pickle
from logging import getLogger

import pylibmc

from .keys import Key

logger = getLogger(__name__)


class MemcacheCache:
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

    def get(self, key: Key) -> Optional[Any]:
        cache_contents = self._mc.get(b"".join(key.as_bytes()))
        if cache_contents is not None:
            return pickle.loads(cache_contents)
        else:
            return None

    def set(self, key: Key, value: Any, ttl: timedelta = timedelta(0)) -> None:
        self._mc.set(b"".join(key.as_bytes()), pickle.dumps(value))

    def invalidate(self, key: Key) -> None:
        ...

    def clear(self) -> None:
        ...
