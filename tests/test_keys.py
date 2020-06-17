import pytest

from pyappcache.keys import SimpleKey, Key


def test_simple_key_to_bytes():
    key: Key[None] = SimpleKey("freddie")
    assert key.as_bytes() == [b"freddie"]


def test_simple_key_repr():
    key: Key[None] = SimpleKey("freddie")
    assert repr(key) == "<SimpleKey 'freddie'>"
