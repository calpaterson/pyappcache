from pyappcache.compression import GZIPCompressor

import pytest


@pytest.fixture(scope="session")
def compressor():
    return GZIPCompressor()


def test_compress_and_decompress(compressor):
    bytestr = b"hello, world"
    assert compressor.decompress(compressor.compress(bytestr)) == bytestr
