from typing import Type

from pyappcache.sqlite import SqliteCache
from pyappcache.keys import SimpleKey, Key

StringToStringKey: Type[Key[str, str]] = SimpleKey


def test_sqlite3_lru():
    """Test that the LRU functionality for SQLite3Cache works right by causing
    an eviction."""
    cache = SqliteCache(max_size=5)

    for i in range(6):
        cache.set(StringToStringKey(str(i)), "something")

    assert cache.get(StringToStringKey("0")) is None


def test_sqlite_lru_with_backing_file(tmp_path):
    """Test that it works with a backing file (as opposed to the default, in
    memory option)"""
    path = tmp_path / "cache.sqlite3"

    cache = SqliteCache(max_size=5, connection_string=path)

    cache.set(StringToStringKey("a"), "b")

    assert path.exists()
