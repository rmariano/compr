"""Tests for the set of functions defined in compressor.functions"""
import sys
import tempfile

from compressor.util import (default_filename, endianess_prefix, pack,
                             tobinary, unpack, StreamFile)


def test_endianess_prefix_bigendinan(monkeypatch):
    monkeypatch.setattr(sys, 'byteorder', 'big')
    assert endianess_prefix() == '>'


def test_endianess_prefix_littleendian(monkeypatch):
    monkeypatch.setattr(sys, 'byteorder', 'little')
    assert endianess_prefix() == '<'


def test_endianess_prefix_bytes(monkeypatch):
    monkeypatch.setattr(sys, 'byteorder', 'big')
    assert endianess_prefix(bytes) == b'>'


def test_littleendian_bytes(monkeypatch):
    monkeypatch.setattr(sys, 'byteorder', 'little')
    assert endianess_prefix(bytes) == b'<'


def test_packing(monkeypatch):
    monkeypatch.setattr(sys, 'byteorder', 'big')

    buffer = pack('i', 42)
    data, = unpack('i', buffer)
    assert data == 42


def test_default_filename_base_file():
    assert default_filename('file') == 'file.comp'


def test_default_filename_abs_path():
    got = default_filename('/usr/local/bin/custom_filename.txt')
    assert got == 'custom_filename.txt.comp'


def test_default_filename_different_suffix():
    assert default_filename('base', 'extr') == 'base.extr'


def test_default_abs_filename_different_suffix():
    assert default_filename('/usr/local/file', 'extr') == 'file.extr'
    assert default_filename('/usr/loca/f2', suffix='foo') == 'f2.foo'


def test_tobinary_int():
    assert tobinary(0xff) == '11111111'
    assert tobinary(42) == '101010'


def test_tobinary_string():
    assert tobinary('ff') == '11111111'
    assert tobinary('F') == tobinary(15)


def test_tobinary_bytes():
    assert tobinary(b'ff') == tobinary(255)
    assert tobinary(b'A') == '1010'


def test_stream_file_chunks():
    with tempfile.NamedTemporaryFile() as data:
        for i in range(10):
            data.write(b"i")
        data.flush()

        with StreamFile(data.name, chunk_size=1) as buffered:
            composed = list(buffered)

    assert composed == ["i" for _ in range(10)]


def test_streamed_file_closed():
    with tempfile.NamedTemporaryFile() as data:
        data.write(b"something")
        data.flush()

        with StreamFile(data.name, chunk_size=10) as buffered:
            list(buffered)

        assert buffered._data_source.closed
