import io
from typing import Optional, cast, IO
from logging import getLogger
from pathlib import Path
import shutil

from .cache import Cache

logger = getLogger(__name__)

# FIXME: respect ttls
# FIXME: allow setting a max cache size
class FilesystemCache(Cache):
    def __init__(self, directory: Path):
        super().__init__()
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

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
