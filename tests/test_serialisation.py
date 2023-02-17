from io import BytesIO

import pandas as pd
from pandas.testing import assert_frame_equal

from .conftest import test_data

from pyappcache.serialisation import PickleSerialiser
from pyappcache.serialisation.pandas import DataFrameAwareSerialiser

stock_exchanges = pd.read_parquet(test_data / "stock-exchanges.parquet")


def test_pickle_serialiser():
    serialiser = PickleSerialiser()
    loaded = serialiser.load(serialiser.dump(BytesIO(b"a"))).read()
    assert loaded == b"a"


def test_dataframe_serialiser_doesnt_change_df():
    serialiser = DataFrameAwareSerialiser()
    loaded = serialiser.load(serialiser.dump(stock_exchanges))
    assert_frame_equal(loaded, stock_exchanges)


def test_dataframe_serialiser_handles_junk():
    serialiser = DataFrameAwareSerialiser()
    assert serialiser.load(BytesIO(b"junk")) is None


def test_dataframe_serialised_handles_normal_objects():
    serialiser = DataFrameAwareSerialiser()
    loaded = serialiser.load(serialiser.dump(BytesIO(b"a"))).read()
    assert loaded == b"a"
