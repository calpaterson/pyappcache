from typing import Any, IO
from io import BytesIO
import pickle
from logging import getLogger

from typing_extensions import Protocol

logger = getLogger(__name__)


class Serialiser(Protocol):
    """The protocol for serialisers to follow"""

    def dump(self, obj: Any) -> IO[bytes]:
        """Dumps an arbitrary Python object to a buffer"""
        pass  # pragma: no cover

    def load(self, data: IO[bytes]) -> Any:
        """Restores an arbitrary Python object from bytes, *or `None` if the
        bytes don't make sense*."""
        pass  # pragma: no cover


class PickleSerialiser:
    """A wrapper for pickling.

    The difference between this and pickle.load/pickle.dump is that
    ``PickleSerialiser`` returns None when it can't unpickle - to defend
    against unreadable cache values."""

    #: The pickle protocol level (default 4).  Changing this default value
    #: will be considered a breaking API change.
    pickle_protocol = 4

    def dump(self, obj: Any) -> IO[bytes]:
        buf = BytesIO()
        pickle.dump(obj, buf, protocol=self.pickle_protocol)
        buf.seek(0)
        return buf

    def load(self, data: IO[bytes]) -> Any:
        try:
            value = pickle.load(data)
        except pickle.UnpicklingError:
            logger.warning("unable to unpickle value")
            value = None
        return value


class BinaryFileSerialiser:
    def dump(self, obj: Any) -> IO[bytes]:
        try:
            pos = obj.tell()
            s = obj.read(10)
            obj.seek(pos)
            if type(s) is not bytes:
                raise RuntimeError(
                    "BinaryFileSerializer can only serialise binary files (got a string file)"
                )
            else:
                return obj
        except AttributeError:
            raise RuntimeError(
                f"BinaryFileSerializer can only serialise files, but got a {type(obj)}"
            )

    def load(self, data: IO[bytes]) -> IO[bytes]:
        return data
