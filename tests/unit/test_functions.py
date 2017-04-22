"""Tests for the set of functions defined in compressor.functions"""
import sys

from compressor.functions import (brand_filename, endianess_prefix, pack,
                                  tobinary, unpack)


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


def test_default_filename():
    assert brand_filename('file') == 'file.comp'


def test_tobinary_int():
    assert tobinary(0xff) == '11111111'
    assert tobinary(42) == '101010'


def test_tobinary_string():
    assert tobinary('ff') == '11111111'
    assert tobinary('F') == tobinary(15)


def test_tobinary_bytes():
    assert tobinary(b'ff') == tobinary(255)
    assert tobinary(b'A') == '1010'
