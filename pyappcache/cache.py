from abc import ABCMeta, abstractmethod
from logging import getLogger
from typing import Optional, TypeVar, Any, cast, Callable, Sequence, Mapping

from .compression import Compressor, GZIPCompressor
from .serialisation import Serialiser, PickleSerialiser
from .keys import Key, build_raw_key

V = TypeVar("V")


logger = getLogger(__name__)


class Cache(metaclass=ABCMeta):
    """The standard, cross backend, interface to a cache."""

    def __init__(self, prefix="pyappache"):
        #: A prefix that will be applied to cache keys to allow for multiple
        #: instances of this class to co-exist.  Exact use varies by particular
        #: cache.  Default is `'pyappcache'`.
        self.prefix = prefix
        #: The compressor that will be used when a key asks for compression.
        #: Default is gzip via :class:`.compression.GZIPCompressor`
        self.compressor: Compressor = GZIPCompressor()
        #: The serialiers that will be used to turn Python objects back and
        #: forth into bytes.  The default serialiser is pickle, via
        #: :class:`.serialisation.PickleSerialiser`
        self.serialiser: Serialiser = PickleSerialiser()

    def get(self, key: Key[V]) -> Optional[V]:
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
            return cast(V, self.serialiser.loads(cache_contents))
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

    def get_via(self, key: Key[V], getter: Callable[[], V]) -> V:
        cache_contents = self.get(key)
        if cache_contents is None:
            new_cache_contents = getter()
            self.set(key, new_cache_contents)
            return new_cache_contents
        else:
            return cache_contents

    def lookup_namespace(self, key: Key) -> Optional[str]:
        # FIXME: is this required?
        namespace = self.get(key)
        if namespace is not None:
            return str(namespace)
        else:
            return None

    def set(self, key: Key[V], value: V, ttl_seconds: int = 0) -> None:
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

    def set_via(
        self,
        key: Key[V],
        value: V,
        setter: Callable[..., Any],
        setter_args: Sequence = (),
        setter_kwargs: Optional[Mapping] = None,
    ) -> None:
        if setter_kwargs is None:
            setter_kwargs = {}
        setter(*setter_args, **setter_kwargs)
        self.set(key, value)

    def set_by_str(
        self, key_str: str, value: V, ttl_seconds: int = 0, compress: bool = False
    ) -> None:
        """Set a value by a :class:`str`."""
        as_pickle = self.serialiser.dumps(value)
        if compress:
            as_bytes = self.compressor.compress(as_pickle)
        else:
            as_bytes = as_pickle
        self.set_raw(
            build_raw_key(self.prefix, key_str),
            as_bytes,
            ttl_seconds,
        )

    def invalidate(self, key: Key[V]) -> None:
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
        """Look up a value (as bytes) from a concrete key string.

        :param key_str: the (fully prefixed) key string to look up

        """
        pass  # pragma: no cover

    @abstractmethod
    def set_raw(self, key_str: str, value_bytes: bytes, ttl_seconds: int) -> None:
        """Set a value (as bytes) by a concrete key string.

        :param key_str: the (fully prefixed) key string to set.
        """
        pass  # pragma: no cover

    @abstractmethod
    def invalidate_raw(self, key_str: str) -> None:
        """Invalidate a key by a concrete key string.

        :param key_str: the (fully prefixed) key string to invalidate
        """
        pass  # pragma: no cover

    @abstractmethod
    def clear(self) -> None:
        """Remove all keys from the cache.

        For most caches this will remove absolutely everything from the
        server, so use with care.

        """
        pass  # pragma: no cover
