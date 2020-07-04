import contextlib
import sqlite3

from pyappcache.sqlite import SqliteCache
from .utils import StringToStringKey


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

    with contextlib.closing(sqlite3.connect(str(path))) as connection:
        cache = SqliteCache(max_size=5, connection=connection)

        cache.set(StringToStringKey("a"), "b")

        assert path.exists()
