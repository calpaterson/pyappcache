from pyappcache.compression import DefaultGZIPCompressor

import pytest


@pytest.fixture(scope="session")
def compressor():
    return DefaultGZIPCompressor()


def test_compress_and_decompress(compressor):
    bytestr = b"hello, world"
    assert compressor.decompress(compressor.compress(bytestr)) == bytestr
