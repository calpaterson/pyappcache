from abc import ABCMeta, abstractmethod
from typing import Optional, TypeVar

from .keys import Key, K, V

K_inv = TypeVar("K_inv")
V_inv = TypeVar("V_inv")


class Cache(metaclass=ABCMeta):
    @abstractmethod
    def get(self, key: Key[K_inv, V_inv]) -> Optional[V_inv]:
        pass

    @abstractmethod
    def set(self, key: Key[K_inv, V_inv], value: K_inv, ttl_seconds: int = 0) -> None:
        pass

    @abstractmethod
    def invalidate(self, key: Key[K_inv, V_inv]) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
