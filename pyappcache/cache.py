from abc import ABCMeta, abstractmethod
from typing import Optional, TypeVar

from .keys import Key

K_inv = TypeVar("K_inv")
V_inv = TypeVar("V_inv")


class Cache(metaclass=ABCMeta):
    @abstractmethod
    def get(self, key: Key[V_inv]) -> Optional[V_inv]:
        pass  # pragma: no cover

    @abstractmethod
    def set(self, key: Key[V_inv], value: V_inv, ttl_seconds: int = 0) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def invalidate(self, key: Key[V_inv]) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def clear(self) -> None:
        pass  # pragma: no cover
