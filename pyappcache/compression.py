import gzip


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
