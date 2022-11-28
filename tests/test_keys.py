from pyappcache.serialisation import PickleSerialiser
from pyappcache.keys import SimpleStringKey, Key
from .utils import StringToIntKey


def test_simple_key_to_segments():
    key = StringToIntKey("freddie")
    assert key.cache_key_segments() == ["freddie"]


def test_should_compress():
    key = StringToIntKey("freddie")
    obj = 1
    as_bytes = PickleSerialiser().dumps(obj)
    assert key.should_compress(obj, as_bytes) is False


def test_simple_string_key_repr():
    key: Key[str] = SimpleStringKey("foo")
    assert repr(key) == "<SimpleStringKey 'foo'>"
