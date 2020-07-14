import gzip


class DefaultGZIPCompressor:
    """A default compressor that is gzip at level 5."""

    def is_compressed(self, data: bytes) -> bool:
        return data[:2] == b"\x1f\x8b"

    def compress(self, data: bytes) -> bytes:
        return gzip.compress(data, compresslevel=5)

    def decompress(self, data: bytes) -> bytes:
        return gzip.decompress(data)
