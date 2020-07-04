from .utils import StringToIntKey


def test_simple_key_to_segments():
    key = StringToIntKey("freddie")
    assert key.as_segments() == ["freddie"]


def test_simple_key_repr():
    key = StringToIntKey("freddie")
    assert repr(key) == "<GenericStringKey 'freddie'>"
