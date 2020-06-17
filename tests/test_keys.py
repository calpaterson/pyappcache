from typing import Type
from pyappcache.keys import SimpleKey, Key

StringToIntKey: Type[Key[str, int]] = SimpleKey


def test_simple_key_to_bytes():
    key = StringToIntKey("freddie")
    assert key.as_bytes() == [b"freddie"]


def test_simple_key_repr():
    key = StringToIntKey("freddie")
    assert repr(key) == "<SimpleKey 'freddie'>"
