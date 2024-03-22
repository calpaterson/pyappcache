from io import BytesIO, StringIO

import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from .conftest import test_data

from pyappcache.serialisation import PickleSerialiser, BinaryFileSerialiser
from pyappcache.serialisation.pandas import DataFrameAwareSerialiser

stock_exchanges = pd.read_parquet(test_data / "stock-exchanges.parquet")


def test_pickle_serialiser():
    serialiser = PickleSerialiser()
    loaded = serialiser.load(serialiser.dump(BytesIO(b"a"))).read()
    assert loaded == b"a"


def test_dataframe_serialiser__doesnt_change_df():
    serialiser = DataFrameAwareSerialiser()
    loaded = serialiser.load(serialiser.dump(stock_exchanges))
    assert_frame_equal(loaded, stock_exchanges)


def test_dataframe_serialiser__handles_junk():
    serialiser = DataFrameAwareSerialiser()
    assert serialiser.load(BytesIO(b"junk")) is None


def test_dataframe_serialised__handles_normal_objects():
    serialiser = DataFrameAwareSerialiser()
    loaded = serialiser.load(serialiser.dump(BytesIO(b"a"))).read()
    assert loaded == b"a"

def test_binary_file_serialiser__works_on_files():
    serialiser = BinaryFileSerialiser()
    buf = BytesIO(b"hello")
    assert serialiser.dump(buf).getvalue() == b"hello"

    assert serialiser.load(buf).getvalue() == b"hello"


def test_binary_file_serialiser__explodes_on_objects():
    serialiser = BinaryFileSerialiser()
    with pytest.raises(RuntimeError):
        serialiser.dump({})


def test_binary_file_serialiser__explodes_on_text_file():
    serialiser = BinaryFileSerialiser()
    buf = StringIO("hello")
    with pytest.raises(RuntimeError):
        serialiser.dump(buf)
