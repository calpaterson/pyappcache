from typing import Optional, Union, IO
import shutil
import io
from datetime import datetime, timedelta
from contextlib import closing
import sqlite3

from dateutil.parser import parse as parse_dt

from .cache import Cache

CREATE_DDL = """
CREATE TABLE IF NOT EXISTS pyappcache
(key PRIMARY KEY, value NOT NULL, expiry NOT NULL, last_read NOT NULL);
"""

INDEX_DDL = [
    """
    CREATE INDEX IF NOT EXISTS pyappcache_expiry
    ON pyappcache (expiry);
    """,
    """
    CREATE INDEX IF NOT EXISTS pyappcache_last_read
    ON pyappcache (last_read);
    """,
]

SET_DML = """
INSERT OR REPLACE INTO pyappcache
(key, value, expiry, last_read)
VALUES
(?, ?, ?, ?);
"""

EVICT_DML = """
DELETE FROM pyappcache
WHERE key IN (
SELECT key
FROM pyappcache
ORDER BY last_read DESC
LIMIT -1 OFFSET ?
);
"""

TOUCH_DML = """
UPDATE pyappcache
SET last_read = ?
WHERE key = ?
AND (expiry >= ? OR expiry = '-1');
"""

GET_DQL = """
SELECT value
FROM pyappcache
WHERE key = ?
AND (expiry >= ? OR expiry = '-1');
"""

GET_DQL_FOR_BLOBOPEN = """
SELECT rowid
FROM pyappcache
WHERE key = ?
AND (expiry >= ? OR expiry = '-1');
"""

GET_TTL_DQL = """
SELECT expiry
FROM pyappcache
WHERE key = ?;
"""

INVALIDATE_DML = """
DELETE FROM pyappcache
WHERE key = ?;
"""

CLEAR_DML = """
DELETE FROM pyappcache;
"""

# This is present as a basic safety feature - to prevent people blowing up
# their processes by accident
MAX_SIZE = 10_000


_in_memory_conn = None


def get_in_memory_conn():
    """Get a shared in-memory connection.

    This is used by :class:`~pyappcache.sqlite_lru.SqliteCache` to get a named
    in-memory sqlite connection (`pyappcache_memory` - to avoid clobbering
    other users of in-memory sqlite databases) and multi-thread support.

    """
    global _in_memory_conn
    if _in_memory_conn is None:
        # This avoids clobbering other in memory sqlite databases (but allows
        # us to use them from different threads)
        _in_memory_conn = sqlite3.connect(
            "file:pyappcache_memory?mode=memory&cache=shared"
        )
    return _in_memory_conn


class SqliteCache(Cache):
    """Implementation of an LRU cache using sqlite3.

    Note that as this is an LRU cache data accesses require write access (in
    order to update the last-used time).
    """

    def __init__(
        self, max_size: int = MAX_SIZE, connection: Optional[sqlite3.Connection] = None
    ):
        """

        :parameter max_size: Maximum size of the LRU cache.  Defaults to 10,000
        :parameter connection: Optionally, you can pass a sqlite3 connection. By
            default an in-memory database will be used (this will be is shared between all
            instances).

        """
        super().__init__()
        if connection is None:
            self.conn = get_in_memory_conn()
        else:
            self.conn = connection
        self.max_size = max_size
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(CREATE_DDL)
            for index_ddl in INDEX_DDL:
                cursor.execute(index_ddl)
            self.conn.commit()

    def get_raw(self, raw_key: str) -> Optional[IO[bytes]]:
        now = datetime.utcnow()
        has_blobopen = hasattr(self.conn, "blobopen")
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(TOUCH_DML, (now, raw_key, now))
            if has_blobopen:
                cursor.execute(GET_DQL_FOR_BLOBOPEN, (raw_key, now))
            else:
                cursor.execute(GET_DQL, (raw_key, now))
            v = cursor.fetchone()
        if v is not None:
            if has_blobopen:
                rowid = v[0]
                blob = self.conn.blobopen("pyappcache", "value", rowid, readonly=True)
                # we need readline above in the stack, for pickle.
                # frustratingly sqlite3.Blob does not have that and none of the
                # wrappers in io seem able to polyfill it
                rv = io.BytesIO()
                shutil.copyfileobj(blob, rv)
                rv.seek(0)
            else:
                (cache_contents,) = v
                rv = io.BytesIO(cache_contents)
        else:
            rv = None
        self.conn.commit()
        return rv

    def set_raw(self, key_bytes: str, value_bytes: IO[bytes], ttl: int) -> None:
        last_read = datetime.utcnow()
        expiry: Union[str, datetime]
        if ttl != 0:
            expiry = last_read + timedelta(seconds=ttl)
        else:
            expiry = "-1"
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(SET_DML, (key_bytes, value_bytes.read(), expiry, last_read))
            cursor.execute(EVICT_DML, (self.max_size,))
            self.conn.commit()

    def ttl(self, key_bytes: str) -> Optional[int]:
        now = datetime.utcnow()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(GET_TTL_DQL, (key_bytes,))
            (expiry,) = cursor.fetchone()
        expiry_dt = parse_dt(expiry)
        ttl_td = expiry_dt - now
        return int(ttl_td.total_seconds())

    def invalidate_raw(self, raw_key: str) -> None:
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(INVALIDATE_DML, (raw_key,))
            self.conn.commit()

    def clear(self) -> None:
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(CLEAR_DML)
            self.conn.commit()
