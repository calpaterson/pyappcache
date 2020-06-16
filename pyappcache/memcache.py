from datetime import timedelta
from typing import Sequence, Mapping, Optional, Any
import pickle
from logging import getLogger

import pylibmc

from .keys import Key

logger = getLogger(__name__)


class MemcacheCache:
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
        return pickle.loads(self._mc.get(b"".join(key.as_bytes())))

    def set(self, key: Key, value: Any, ttl: timedelta = timedelta(0)) -> None:
        self._mc.set(b"".join(key.as_bytes()), pickle.dumps(value))

    def invalidate(self, key: Key) -> None:
        ...

    def clear(self) -> None:
        ...
