import pytest

from pyappcache.keys import SimpleKey, Key


def test_simple_key_to_bytes():
    key = SimpleKey("freddie")
    assert key.as_bytes() == [b"freddie"]


def test_simple_key_repr():
    key = SimpleKey("freddie")
    assert repr(key) == "<SimpleKey 'freddie'>"
