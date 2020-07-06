import gzip


class DefaultGZIPCompressor:
    """A default compressor that is gzip at level 5."""

    def compress(self, data: bytes) -> bytes:
        ...

    def decompress(self, data: bytes) -> bytes:
        ...
