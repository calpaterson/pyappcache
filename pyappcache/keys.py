from typing import TypeVar, Sequence
from typing_extensions import Protocol

V = TypeVar("V", covariant=True)


class Key(Protocol[V]):
    def as_segments(self) -> Sequence[str]:
        pass  # pragma: no cover


class GenericStringKey(Key[V]):
    def __init__(self, key_str: str):
        self.key_str = key_str

    def __repr__(self):
        return f"<GenericStringKey '{self.key_str}'>"

    def as_segments(self) -> Sequence[str]:
        return [self.key_str]


def build_raw_key(prefix: str, key: Key) -> str:
    key_segments = [prefix]
    key_segments.extend(key.as_segments())
    key_bytes = "".join(key_segments)
    return key_bytes
