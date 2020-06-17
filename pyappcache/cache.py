from abc import ABCMeta, abstractmethod
from typing import Optional, TypeVar

from .keys import Key

S_inv = TypeVar("S_inv")


class Cache(metaclass=ABCMeta):
    @abstractmethod
    def get(self, key: Key[S_inv]) -> Optional[S_inv]:
        pass

    @abstractmethod
    def set(self, key: Key[S_inv], value: S_inv, ttl_seconds: int) -> None:
        pass

    @abstractmethod
    def invalidate(self, key: Key[S_inv]) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
