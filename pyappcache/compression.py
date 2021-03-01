import gzip

from typing_extensions import Protocol


class Compressor(Protocol):
    """The protocol for compressors to follow"""

    def is_compressed(self, data: bytes) -> bool:
        """Takes some, possibly compressed data as an argument and returns True
        if is has been compressed with this compressor, False otherwise."""
        pass  # pragma: no cover

    def compress(self, data: bytes) -> bytes:
        """Compress the given bytes with this compressor"""
        pass  # pragma: no cover

    def decompress(self, data: bytes) -> bytes:
        """Decompress the given bytes with this compressor"""
        pass  # pragma: no cover


class GZIPCompressor:
    """A default compressor that is gzip at level 5."""

    def __init__(self, level: int = 5):
        """

        :param level: The gzip compression level (default 5)"""
        #: Gzip compression level
        self.level = level

    def is_compressed(self, data: bytes) -> bool:
        return data[:2] == b"\x1f\x8b"

    def compress(self, data: bytes) -> bytes:
        return gzip.compress(data, compresslevel=self.level)

    def decompress(self, data: bytes) -> bytes:
        return gzip.decompress(data)
