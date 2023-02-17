from io import BytesIO
import shutil
from typing import IO, cast
import gzip

from typing_extensions import Protocol


class Compressor(Protocol):
    """The protocol for compressors to follow"""

    def is_compressed(self, data: IO[bytes]) -> bool:
        """Takes some, possibly compressed data as an argument and returns True
        if is has been compressed with this compressor, False otherwise."""
        pass  # pragma: no cover

    def compress(self, data: IO[bytes]) -> IO[bytes]:
        """Compress the given bytes with this compressor"""
        pass  # pragma: no cover

    def decompress(self, data: IO[bytes]) -> IO[bytes]:
        """Decompress the given bytes with this compressor"""
        pass  # pragma: no cover


class GZIPCompressor:
    """A default compressor that is gzip at level 5."""

    def __init__(self, level: int = 5):
        """

        :param level: The gzip compression level (default 5)"""
        #: Gzip compression level
        self.level = level

    def is_compressed(self, data: IO[bytes]) -> bool:
        head = data.read(2)
        data.seek(0)
        return head == b"\x1f\x8b"

    def compress(self, data: IO[bytes]) -> IO[bytes]:
        inner_buf = BytesIO()
        with gzip.GzipFile(
            fileobj=inner_buf, mode="w", compresslevel=self.level
        ) as gzip_f:
            shutil.copyfileobj(data, gzip_f)
        inner_buf.seek(0)
        return inner_buf

    def decompress(self, data: IO[bytes]) -> IO[bytes]:
        return cast(IO[bytes], gzip.open(data))
