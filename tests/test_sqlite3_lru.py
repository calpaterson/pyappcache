from typing import Type

from pyappcache.sqlite import SqliteCache
from pyappcache.keys import SimpleKey, Key

import pytest


StringToStringKey: Type[Key[str, str]] = SimpleKey


def test_sqlite3_lru():
    """Test that the LRU functionality for SQLite3Cache works right by causing
    an eviction."""
    cache = SqliteCache(max_size=5)

    for i in range(6):
        cache.set(StringToStringKey(str(i)), "something")

    assert cache.get(StringToStringKey("0")) is None


@pytest.mark.xfail(reason="test not implemented")
def test_sqlite_lru_with_backing_file(tmpdir):
    """Test that it works with a backing file (as opposed to the default, in
    memory option)"""
    assert False
