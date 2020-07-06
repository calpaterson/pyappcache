import contextlib
import sqlite3

from pyappcache.sqlite_lru import SqliteCache
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


def test_in_memory_db_naming():
    """Test that our in memory sqlite db does not clash with ordinary
    ':memory:' sqlite databases."""
    cache = SqliteCache()

    cache.set(StringToStringKey("a"), "b")

    table_dql = """
    SELECT name FROM sqlite_master WHERE type = 'table';
    """
    in_memory_conn = sqlite3.connect(":memory:")
    tables = in_memory_conn.execute(table_dql).fetchall()

    assert len(tables) == 0
