from typing import List, TypeVar, Sequence
from typing_extensions import Protocol

S = TypeVar("S", covariant=True)


class Key(Protocol[S]):
    def __init__(self, key_subject: S) -> None:
        ...

    def as_bytes(self) -> Sequence[bytes]:
        ...


class SimpleKey(Key[S]):
    def __init__(self, key_str: str):
        self.key_str = key_str

    def __repr__(self):
        return f"<SimpleKey '{self.key_str}'>"

    def as_bytes(self) -> Sequence[bytes]:
        return [bytes(self.key_str, "utf-8")]
