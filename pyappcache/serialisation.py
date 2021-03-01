from typing import Any
import pickle
from logging import getLogger

from typing_extensions import Protocol

logger = getLogger(__name__)


class Serialiser(Protocol):
    """The protocol for serialisers to follow"""

    def dumps(self, obj: Any) -> bytes:
        """Dumps an arbitrary Python object to bytes"""
        pass  # pragma: no cover

    def loads(self, data: bytes) -> Any:
        """Restores an arbitrary Python object from bytes, *or `None` if the
        bytes don't make sense*."""
        pass  # pragma: no cover


class PickleSerialiser:
    """A wrapper for pickling.

    The difference between this and pickle.loads/pickle.dumps is that
    ``PickleSerialiser`` returns None when it can't unpickle - to defend
    against unreadable cache values."""

    #: The pickle protocol level (default 4).  Changing this default value
    #: will be considered a breaking API change.
    pickle_protocol = 4

    def dumps(self, obj: Any) -> bytes:
        return pickle.dumps(obj, protocol=self.pickle_protocol)

    def loads(self, data: bytes) -> Any:
        try:
            value = pickle.loads(data)
        except pickle.UnpicklingError:
            logger.warning("unable to unpickle value")
            value = None
        return value
