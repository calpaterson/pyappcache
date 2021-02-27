from typing import Any
import pickle
from logging import getLogger

logger = getLogger(__name__)


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
