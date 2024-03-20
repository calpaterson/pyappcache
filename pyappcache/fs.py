import sqlite3
from typing import Optional, IO, List
from logging import getLogger
from pathlib import Path
import shutil
from contextlib import closing

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

INDEX_DDL: List[str] = []

# FIXME: respect ttls
# FIXME: allow setting a max cache size
class FilesystemCache(Cache):
    METADATA_DB_FILENAME = "metadata.sqlite3"

    def __init__(self, directory: Path):
        super().__init__()
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.directory / "metadata.sqlite"))
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(CREATE_DDL)
            for index_ddl in INDEX_DDL:
                cursor.execute(index_ddl)
            self.conn.commit()


    def _make_path(self, raw_key: str) -> Path:
        path = self.directory / raw_key.replace("/", "_")
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def get_raw(self, raw_key: str) -> Optional[IO[bytes]]:
        path = self._make_path(raw_key)
        try:
            return path.open("rb")
        except FileNotFoundError:
            return None

    def set_raw(self, raw_key: str, value_bytes: IO[bytes], ttl_seconds: int) -> None:
        path = self._make_path(raw_key)
        with path.open("w+b") as fh:
            shutil.copyfileobj(value_bytes, fh)

    def invalidate_raw(self, raw_key: str) -> None:
        path = self._make_path(raw_key)
        path.unlink(missing_ok=True)

    def clear(self) -> None:
        shutil.rmtree(self.directory)
