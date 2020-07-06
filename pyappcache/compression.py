import gzip


class DefaultGZIPCompressor:
    """A default compressor that is gzip at level 5."""

    def compress(self, data: bytes) -> bytes:
        return gzip.compress(data, compresslevel=5)

    def decompress(self, data: bytes) -> bytes:
        return gzip.decompress(data)
