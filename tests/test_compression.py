from io import BytesIO

from pyappcache.compression import GZIPCompressor

import pytest


@pytest.fixture(scope="session")
def compressor():
    return GZIPCompressor()


def test_compress_and_decompress(compressor):
    buf = BytesIO(b"hello, world")
    decompressed = compressor.decompress(compressor.compress(buf)).read()
    buf.seek(0)
    expected = buf.read()
    assert expected == decompressed
