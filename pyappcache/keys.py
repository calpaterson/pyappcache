from typing import TypeVar, Sequence
from typing_extensions import Protocol

V = TypeVar("V", covariant=True)


class Key(Protocol[V]):
    def as_bytes(self) -> Sequence[bytes]:
        pass  # pragma: no cover


class GenericStringKey(Key[V]):
    def __init__(self, key_str: str):
        self.key_str = key_str

    def __repr__(self):
        return f"<GenericStringKey '{self.key_str}'>"

    def as_bytes(self) -> Sequence[bytes]:
        return [bytes(self.key_str, "utf-8")]


def build_raw_key(prefix: bytes, key: Key) -> bytes:
    key_segments = [prefix]
    key_segments.extend(key.as_bytes())
    key_bytes = b"".join(key_segments)
    return key_bytes
