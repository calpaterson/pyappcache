import os
import sqlite3
from typing import Optional, IO, List
from logging import getLogger
from pathlib import Path
import shutil
from contextlib import closing
from datetime import datetime, timedelta

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

INDEX_DDL: List[str] = []

# FIXME: respect ttls
# FIXME: allow setting a max cache size
class FilesystemCache(Cache):
    METADATA_DB_FILENAME = "metadata.sqlite3"

    def __init__(self, directory: Path):
        super().__init__()
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)
        self.metadata_conn = sqlite3.connect(str(self.directory / "metadata.sqlite"))
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
        self.clear_expired()
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

    def invalidate_raw(self, raw_key: str) -> None:
        path = self._make_path(raw_key)
        path.unlink(missing_ok=True)

    def clear_expired(self) -> None:
        with closing(self.metadata_conn.cursor()) as cursor:
            cursor.execute(GET_EXPIRED_DQL)
            for raw_key, in cursor.fetchall():
                self.invalidate_raw(raw_key)
                cursor.execute(REMOVE_EXPIRED_DML, [raw_key])

    def clear(self) -> None:
        shutil.rmtree(self.directory)

def _get_fh_size(fh: IO[bytes]) -> int:
    pos = fh.tell()
    fh.seek(0, os.SEEK_END)
    size = fh.tell()
    fh.seek(pos)
    return size
