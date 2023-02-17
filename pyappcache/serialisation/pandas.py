from logging import getLogger

logger = getLogger(__name__)

from typing import Any, IO
from io import BytesIO

import pandas as pd

from .core import PickleSerialiser


class DataFrameAwareSerialiser(PickleSerialiser):
    """A serialiser that is aware of dataframes and, instead of pickling them,
    outputs them to parquet.

    """

    def __init__(self):
        super().__init__()

    def dump(self, obj: Any) -> IO[bytes]:
        if isinstance(obj, pd.DataFrame):
            buf = BytesIO()
            obj.to_parquet(buf)
            buf.seek(0)
            return buf
        else:
            return super().dump(obj)

    def load(self, data: IO[bytes]) -> Any:
        if _is_parquet(data):
            return pd.read_parquet(data)
        else:
            return super().load(data)


def _is_parquet(data: IO[bytes]) -> bool:
    head = data.read(3)
    data.seek(0)
    return head == b"PAR"
