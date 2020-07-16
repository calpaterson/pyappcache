from typing import TypeVar, Sequence, Union, Optional, Any
from typing_extensions import Protocol

V = TypeVar("V", contravariant=True)


class Key(Protocol[V]):
    def namespace_key(self) -> "Optional[Key[Any]]":
        pass  # pragma: no cover

    # FIXME: should should_compress be required?  or just an optional thing to
    # implement
    def should_compress(self, python_obj: V, as_bytes: bytes) -> bool:
        pass  # pragma: no cover

    def as_segments(self) -> Sequence[str]:
        pass  # pragma: no cover


# FIXME: is it possible to make this a KeyBase or something?
class GenericStringKey(Key[V]):
    def __init__(self, key_str: str):
        self.key_str = key_str

    def namespace_key(self) -> Optional[Key[Any]]:
        return None

    def should_compress(self, python_obj: V, as_bytes: bytes) -> bool:
        return False

    def as_segments(self) -> Sequence[str]:
        return [self.key_str]


def build_raw_key(
    prefix: str, key: Union[Key, str], namespace: Optional[str] = None
) -> str:
    """Creates a string key from a cache prefix and a key, and optionally a
    resolved namespace.
    """
    key_segments = [prefix]
    if namespace is not None:
        key_segments.append(namespace)
    if isinstance(key, str):
        key_segments.append(key)
    else:
        key_segments.extend(key.as_segments())
    key_str = "/".join(key_segments)
    return key_str
