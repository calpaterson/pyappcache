from abc import ABCMeta, abstractmethod
from logging import getLogger
from typing import Optional, TypeVar, Any, cast

from .compression import DefaultGZIPCompressor
from .serialisation import PickleSerialiser
from .keys import Key, build_raw_key

V_inv = TypeVar("V_inv")


logger = getLogger(__name__)


class Cache(metaclass=ABCMeta):
    """Abstract base class for all caches.

    :ivar prefix: A prefix that will be applied to cache keys to allow for multiple instances of this class to co-exist.  Exact use varies by particular cache.  Default is `'pyappcache'`.
    :ivar compressor: The compressor that will be used when a key asks for compression.
    :ivar serialiser: The serialiers that will be used to turn Python objects back and forth into bytes

    """
    def __init__(self):
        self.prefix = "pyappcache"
        self.compressor = DefaultGZIPCompressor()
        self.serialiser = PickleSerialiser()

    def get(self, key: Key[V_inv]) -> Optional[V_inv]:
        """Look up the value stored under a :class:`~pyappcache.keys.Key` instance"""
        namespace_key = key.namespace_key()
        if namespace_key is not None:
            namespace = self.lookup_namespace(namespace_key)
            if namespace is None:
                return None
        else:
            namespace = None

        cache_contents = self.get_raw(
            build_raw_key(self.prefix, key, namespace=namespace)
        )
        if cache_contents is not None:
            if self.compressor.is_compressed(cache_contents):
                cache_contents = self.compressor.decompress(cache_contents)
            return cast(V_inv, self.serialiser.loads(cache_contents))
        else:
            return None

    def get_by_str(self, key_str: str) -> Optional[Any]:
        """Look up the value stored under a :class:`str`.

        Users of this method will have to construct string keys for themselves."""
        cache_contents = self.get_raw(build_raw_key(self.prefix, key_str))
        if cache_contents is not None:
            if self.compressor.is_compressed(cache_contents):
                cache_contents = self.compressor.decompress(cache_contents)
            return self.serialiser.loads(cache_contents)
        else:
            return None

    def lookup_namespace(self, key: Key) -> Optional[str]:
        # FIXME: is this required?
        namespace = self.get(key)
        if namespace is not None:
            return str(namespace)
        else:
            return None

    def set(self, key: Key[V_inv], value: V_inv, ttl_seconds: int = 0) -> None:
        """Set a value by :class:`~pyappcache.keys.Key`"""
        namespace_key = key.namespace_key()  # FIXME: move this inside lookup_namespace
        if namespace_key is not None:
            namespace = self.lookup_namespace(namespace_key)
            if namespace is None:
                logger.warning("unable to set key as namespace does not exist")
                return None
        else:
            namespace = None
        as_pickle = self.serialiser.dumps(value)
        if key.should_compress(value, as_pickle):
            as_bytes = self.compressor.compress(as_pickle)
        else:
            as_bytes = as_pickle
        self.set_raw(
            build_raw_key(self.prefix, key, namespace=namespace), as_bytes, ttl_seconds
        )

    def set_by_str(
        self, key_str: str, value: V_inv, ttl_seconds: int = 0, compress: bool = False
    ) -> None:
        """Set a value by a :class:`str`."""
        as_pickle = self.serialiser.dumps(value)
        if compress:
            as_bytes = self.compressor.compress(as_pickle)
        else:
            as_bytes = as_pickle
        self.set_raw(
            build_raw_key(self.prefix, key_str), as_bytes, ttl_seconds,
        )

    def invalidate(self, key: Key[V_inv]) -> None:
        """Invalidate by :class:`~pyappcache.keys.Key`.

        Depending on the particular implementation of invalidation this may or
        may not immediately free memory in the underlying cache (usually not)."""
        namespace_key = key.namespace_key()  # FIXME: move this inside lookup_namespace
        if namespace_key is not None:
            namespace = self.lookup_namespace(namespace_key)
            if namespace is None:
                logger.warning("unable to invalidate key as namespace does not exist")
                return None
        else:
            namespace = None
        self.invalidate_raw(build_raw_key(self.prefix, key, namespace=namespace))

    def invalidate_by_str(self, key_str: str) -> None:
        self.invalidate_raw(build_raw_key(self.prefix, key_str))

    @abstractmethod
    def get_raw(self, key_str: str) -> Optional[bytes]:
        pass  # pragma: no cover

    @abstractmethod
    def set_raw(self, key_str: str, value_bytes: bytes, ttl_seconds: int) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def invalidate_raw(self, key_str: str) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def clear(self) -> None:
        """Remove all keys from the cache.

        For most caches this will remove absolutely everything from the
        server, so use with care."""
        pass  # pragma: no cover
