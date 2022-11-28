from datetime import datetime
import contextlib
import sqlite3

import pytest
import time_machine
from pyappcache.sqlite_lru import SqliteCache
from .utils import StringToStringKey, random_string


@pytest.fixture(scope="function")
def random_conn():
    """A random sqlite3 conn, to prevent clashes between tests"""
    return sqlite3.connect(f"file:{random_string()}?mode=memory&cache=shared")


def test_sqlite3_lru(random_conn):
    """Test that the LRU functionality for SQLite3Cache works right by causing
    an eviction."""
    cache = SqliteCache(max_size=5, connection=random_conn)

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


def test_sqlite3_ttls_cause_expiry(random_conn):
    """Test that TTLs do cause keys to expire"""
    cache = SqliteCache(connection=random_conn)

    key = StringToStringKey("a")
    with time_machine.travel(datetime(2018, 1, 3)):
        cache.set(key, "b", ttl_seconds=1)

    with time_machine.travel(datetime(2018, 1, 4)):
        assert cache.get(key) is None


def test_sqlite3_no_ttls_never_expire(random_conn):
    """Test that keys set with a 0 ttl never expire"""
    cache = SqliteCache(connection=random_conn)

    key = StringToStringKey("a")
    with time_machine.travel(datetime(2018, 1, 3)):
        cache.set(key, "1")

    with time_machine.travel(datetime(2019, 1, 3)):
        assert cache.get(key) == "1"


def test_sqlite3_eviction_with_ttls(random_conn):
    """Test that evictions happen in order of last_read, not ttl"""
    cache = SqliteCache(max_size=1, connection=random_conn)

    key_a = StringToStringKey("a")
    with time_machine.travel(datetime(2018, 1, 3, 0)):
        cache.set(key_a, "1", ttl_seconds=36000)

    key_b = StringToStringKey("b")
    with time_machine.travel(datetime(2018, 1, 3, 1)):
        cache.set(key_b, "2", ttl_seconds=10)

        assert cache.get(key_a) is None
        assert cache.get(key_b) == "2"


def test_sqlite3_eviction_without_ttls(random_conn):
    cache = SqliteCache(max_size=1, connection=random_conn)

    key_a = StringToStringKey("a")
    with time_machine.travel(datetime(2018, 1, 3, 0)):
        cache.set(key_a, "1")

    key_b = StringToStringKey("b")
    with time_machine.travel(datetime(2018, 1, 3, 1)):
        cache.set(key_b, "2")

        assert cache.get(key_a) is None
        assert cache.get(key_b) == "2"


def test_sqlite3_eviction_via_last_read(random_conn):
    cache = SqliteCache(max_size=2, connection=random_conn)

    with time_machine.travel(datetime(2018, 1, 3, 0)):
        key_a = StringToStringKey("a")
        cache.set(key_a, "1", ttl_seconds=36000)

    with time_machine.travel(datetime(2018, 1, 3, 1)):
        key_b = StringToStringKey("b")
        cache.set(key_b, "2", ttl_seconds=36000)

    with time_machine.travel(datetime(2018, 1, 3, 2)):
        cache.get(key_a)

    with time_machine.travel(datetime(2018, 1, 3, 3)):
        key_c = StringToStringKey("c")
        cache.set(key_c, "3", ttl_seconds=36000)

        assert cache.get(key_b) is None
        assert cache.get(key_a) == "1"
