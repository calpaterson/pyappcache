from abc import ABCMeta, abstractmethod
from typing import Optional, TypeVar, Any

from .compression import DefaultGZIPCompressor
from .serialisation import PickleSerialiser
from .keys import Key

K_inv = TypeVar("K_inv")
V_inv = TypeVar("V_inv")


class Cache(metaclass=ABCMeta):
    def __init__(self):
        self.prefix = "/pyappcache/"
        self.compressor = DefaultGZIPCompressor()
        self.serialiser = PickleSerialiser()

    @abstractmethod
    def get(self, key: Key[V_inv]) -> Optional[V_inv]:
        pass  # pragma: no cover

    @abstractmethod
    def get_by_str(self, key_str: str) -> Any:
        pass  # pragma: no cover

    @abstractmethod
    def set(self, key: Key[V_inv], value: V_inv, ttl_seconds: int = 0) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def set_by_str(self, key: str, value: V_inv, ttl_seconds: int = 0) -> None:
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
