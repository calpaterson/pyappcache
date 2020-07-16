from pyappcache.serialisation import PickleSerialiser
from .utils import StringToIntKey


def test_simple_key_to_segments():
    key = StringToIntKey("freddie")
    assert key.as_segments() == ["freddie"]


def test_should_compress():
    key = StringToIntKey("freddie")
    obj = 1
    as_bytes = PickleSerialiser().dumps(obj)
    assert key.should_compress(obj, as_bytes) is False
