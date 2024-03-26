import os
import sqlite3
from typing import Optional, IO, List
from logging import getLogger
from pathlib import Path
import shutil
from contextlib import closing
from datetime import datetime, timedelta

from dateutil.parser import parse as parse_dt

from .cache import Cache

logger = getLogger(__name__)

CREATE_DDL = """
CREATE TABLE IF NOT EXISTS pyappcache (
    key PRIMARY KEY,
    expiry NOT NULL,
    last_read NOT NULL,
    size NOT NULL
);
"""

GET_EXPIRED_DQL = """
SELECT key FROM pyappcache where expiry < CURRENT_TIMESTAMP AND expiry != '-1';
"""

REMOVE_EXPIRED_DML = """
DELETE FROM pyappcache WHERE key = ?
"""

SET_DML = """
INSERT OR REPLACE INTO pyappcache
(key, expiry, last_read, size)
VALUES
(?, ?, ?, ?);
"""

GET_TTL_DQL = """
SELECT expiry
FROM pyappcache
WHERE key = ?;
"""

# The below SQL should be done in one step using the RETURNING clause of the
# DELETE statement, but RETURNING was only added to sqlite in 3.35.0
# (2021-03-12) and not everyone has it yet (including me)

GET_EVICTION_COHORT_DQL = """
SELECT
    KEY
FROM (
    SELECT
        KEY,
        last_read,
        SUM(size) OVER (ORDER BY last_read DESC) AS total_size
    FROM pyappcache) AS t
WHERE
    total_size > ?;
"""

EVICT_COHORT_DML = """
DELETE FROM pyappcache
WHERE KEY IN (
SELECT
    KEY
FROM (
    SELECT
        KEY,
        last_read,
        SUM(size) OVER (ORDER BY last_read DESC) AS total_size
    FROM pyappcache) AS t
WHERE
    total_size > ?
)
"""

INDEX_DDL: List[str] = []


class FilesystemCache(Cache):
    METADATA_DB_FILENAME = "metadata.sqlite3"

    # 100mb default limit
    DEFAULT_MAX_SIZE = 1000 * 1000 * 100

    def __init__(self, directory: Path, max_size_bytes: int=DEFAULT_MAX_SIZE):
        super().__init__()
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)
        self.max_size_bytes = max_size_bytes
        self.metadata_conn = sqlite3.connect(
            str(self.directory / self.METADATA_DB_FILENAME)
        )
        with closing(self.metadata_conn.cursor()) as cursor:
            cursor.execute(CREATE_DDL)
            for index_ddl in INDEX_DDL:
                cursor.execute(index_ddl)
            self.metadata_conn.commit()

    def _make_path(self, raw_key: str) -> Path:
        path = self.directory / raw_key.replace("/", "_")
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def get_raw(self, raw_key: str) -> Optional[IO[bytes]]:
        self._clear_expired()
        path = self._make_path(raw_key)
        try:
            return path.open("rb")
        except FileNotFoundError:
            return None
        else:
            # FIXME: should touch here
            pass

    def set_raw(self, raw_key: str, value_bytes: IO[bytes], ttl_seconds: int) -> None:
        path = self._make_path(raw_key)
        with path.open("w+b") as fh:
            shutil.copyfileobj(value_bytes, fh)
        size = _get_fh_size(value_bytes)
        if ttl_seconds != 0:
            expiry = (datetime.utcnow() + timedelta(seconds=ttl_seconds)).isoformat()
        else:
            expiry = "-1"
        with closing(self.metadata_conn.cursor()) as cursor:
            cursor.execute(SET_DML, (raw_key, expiry, datetime.utcnow(), size))
            self.metadata_conn.commit()
        self._clear_expired()
        self._evict()

    def invalidate_raw(self, raw_key: str) -> None:
        # FIXME: this should be updating the metadata
        path = self._make_path(raw_key)
        path.unlink(missing_ok=True)

    def _evict(self) -> None:
        """Evict data to maintain the maximum size."""
        with closing(self.metadata_conn.cursor()) as cursor:
            cursor.execute("BEGIN;")
            cursor.execute(GET_EVICTION_COHORT_DQL, (self.max_size_bytes,))
            rs = cursor.fetchall()
            cursor.execute(EVICT_COHORT_DML, (self.max_size_bytes,))
            self.metadata_conn.commit()

        for row in rs:
            raw_key = row[0]
            path = self._make_path(raw_key)
            path.unlink(missing_ok=True)

    def _clear_expired(self) -> None:
        """Clear out expired data."""
        with closing(self.metadata_conn.cursor()) as cursor:
            cursor.execute(GET_EXPIRED_DQL)
            for (raw_key,) in cursor.fetchall():
                self.invalidate_raw(raw_key)
                cursor.execute(REMOVE_EXPIRED_DML, [raw_key])

    def ttl(self, key_bytes: str) -> Optional[int]:
        """Returns the (remaining) TTL of the given key."""
        now = datetime.utcnow()
        with closing(self.metadata_conn.cursor()) as cursor:
            cursor.execute(GET_TTL_DQL, (key_bytes,))
            row = cursor.fetchone()
        if row is not None:
            expiry = row[0]
            expiry_dt = parse_dt(expiry)
            ttl_td = expiry_dt - now
            return int(ttl_td.total_seconds())
        else:
            return None

    def clear(self) -> None:
        shutil.rmtree(self.directory)


def _get_fh_size(fh: IO[bytes]) -> int:
    """Return the size of a seekable binary filehandle."""
    pos = fh.tell()
    fh.seek(0, os.SEEK_END)
    size = fh.tell()
    fh.seek(pos)
    return size
