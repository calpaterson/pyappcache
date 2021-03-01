from abc import abstractmethod, ABCMeta

from typing import TypeVar, Sequence, Union, Optional, Any
from typing_extensions import Protocol

#: Key value
V = TypeVar("V", contravariant=True)


class Key(Protocol[V]):
    """The "protocol" for keys.  Define the same methods as this class, and you
    have created a key which will work with pyappcache.

    """

    def namespace_key(self) -> "Optional[Key[Any]]":
        """If this is a namespaced key, this method returns the key to the
        namespace that should be used - otherwise None.

        """
        pass  # pragma: no cover

    def should_compress(self, python_obj: V, as_bytes: bytes) -> bool:
        """This method passes the original Python object and the serialised
        `bytes` version of it in order to allow this method to decide whether
        compression should be used.

        This allows for this method to take Python level attributes/methods and
        the size of the bytestring into account when making a decision.

        Returns True if compression should be applied, False if not.
        """
        pass  # pragma: no cover

    def cache_key_segments(self) -> Sequence[str]:
        """Return segments of the whole key path.  For example `["a", "b",
        "c"]` - the key segments will be prepended with the Cache's own
        :attr:`~pyappcache.cache.Cache.prefix` and then joined with slashes,
        similar to unix paths."""
        pass  # pragma: no cover


class BaseKey(Key[V], metaclass=ABCMeta):
    """An abstract baseclass suitable (but not required) for subclassing to
    create many class:`~Key` instances.

    To use, subclass and override :meth:`~cache_key_segments`.  To get
    progressively more functionality, you can also override
    :meth:`~namespace_key` and :meth:`should_compress`.

    """

    def namespace_key(self) -> Optional[Key[Any]]:
        return None

    def should_compress(self, python_obj: V, as_bytes: bytes) -> bool:
        return False

    @abstractmethod
    def cache_key_segments(self) -> Sequence[str]:
        ...  # pragma: no cover


class SimpleStringKey(Key[V]):
    def __init__(self, key_str: str):
        self.key_str = key_str

    def namespace_key(self) -> Optional[Key[Any]]:
        return None

    def should_compress(self, python_obj: V, as_bytes: bytes) -> bool:
        return False

    def cache_key_segments(self) -> Sequence[str]:
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
        key_segments.extend(key.cache_key_segments())
    key_str = "/".join(key_segments)
    return key_str
