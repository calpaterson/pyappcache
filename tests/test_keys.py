from .utils import StringToIntKey


def test_simple_key_to_bytes():
    key = StringToIntKey("freddie")
    assert key.as_bytes() == [b"freddie"]


def test_simple_key_repr():
    key = StringToIntKey("freddie")
    assert repr(key) == "<SimpleKey 'freddie'>"
