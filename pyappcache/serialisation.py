from typing import Any
import pickle
from logging import getLogger

# Changing this constant shall be considered a breaking change
PICKLE_PROTOCOL = 4

logger = getLogger(__name__)


class PickleSerialiser:
    """A wrapper for pickling.

    Compared the pickle.loads this does not raise an exception when a pickle
    cannot be read."""

    def dumps(self, obj: Any) -> bytes:
        return pickle.dumps(obj, protocol=PICKLE_PROTOCOL)

    def loads(self, data: bytes) -> Any:
        try:
            value = pickle.loads(data)
        except pickle.UnpicklingError:
            logger.warning("unable to unpickle value")
            value = None
        return value
