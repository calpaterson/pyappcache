from typing import List
from typing_extensions import Protocol


class Key(Protocol):
    def as_bytes(self) -> List[bytes]: ...


class SimpleKey:
    def __init__(self, key_str: str):
        self.key_str = key_str

    def __repr__(self):
        return f"<SimpleKey '{self.key_str}'>"

    def as_bytes(self):
        return [bytes(self.key_str, "utf-8")]
