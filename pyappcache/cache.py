from abc import ABCMeta, abstractmethod
from typing import Optional, TypeVar, Any, cast

from .compression import DefaultGZIPCompressor
from .serialisation import PickleSerialiser
from .keys import Key, build_raw_key

K_inv = TypeVar("K_inv")
V_inv = TypeVar("V_inv")


class Cache(metaclass=ABCMeta):
    def __init__(self):
        self.prefix = "/pyappcache/"
        self.compressor = DefaultGZIPCompressor()
        self.serialiser = PickleSerialiser()

    def get(self, key: Key[V_inv]) -> Optional[V_inv]:
        cache_contents = self.get_raw(build_raw_key(self.prefix, key))
        if cache_contents is not None:
            if self.compressor.is_compressed(cache_contents):
                cache_contents = self.compressor.decompress(cache_contents)
            return cast(V_inv, self.serialiser.loads(cache_contents))
        else:
            return None

    def get_by_str(self, key_str: str) -> Optional[Any]:
        cache_contents = self.get_raw(build_raw_key(self.prefix, key_str))
        if cache_contents is not None:
            if self.compressor.is_compressed(cache_contents):
                cache_contents = self.compressor.decompress(cache_contents)
            return self.serialiser.loads(cache_contents)
        else:
            return None

    @abstractmethod
    def get_raw(self, key_str: str) -> Optional[bytes]:
        pass  # pragma: no cover

    def set(self, key: Key[V_inv], value: V_inv, ttl_seconds: int = 0) -> None:
        as_pickle = self.serialiser.dumps(value)
        if key.should_compress(value, as_pickle):
            as_bytes = self.compressor.compress(as_pickle)
        else:
            as_bytes = as_pickle
        self.set_raw(build_raw_key(self.prefix, key), as_bytes, ttl_seconds)

    def set_by_str(
        self, key_str: str, value: V_inv, ttl_seconds: int = 0, compress: bool = False
    ) -> None:
        as_pickle = self.serialiser.dumps(value)
        if compress:
            as_bytes = self.compressor.compress(as_pickle)
        else:
            as_bytes = as_pickle
        self.set_raw(
            build_raw_key(self.prefix, key_str), as_bytes, ttl_seconds,
        )

    @abstractmethod
    def set_raw(self, key_bytes: str, value_bytes: bytes, ttl_seconds: int) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def invalidate(self, key: Key[V_inv]) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def invalidate_by_str(self, key_str: str) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def clear(self) -> None:
        pass  # pragma: no cover
