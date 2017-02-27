"""Tests for the set of functions defined in compressor.functions"""
import sys

from compressor.functions import endianess_prefix, pack, unpack, brand_filename


def test_endianess_prefix_bigendinan(monkeypatch):
    monkeypatch.setattr(sys, 'byteorder', 'big')
    assert endianess_prefix() == '>'


def test_endianess_prefix_bytes(monkeypatch):
    monkeypatch.setattr(sys, 'byteorder', 'big')
    assert endianess_prefix(bytes) == b'>'


def test_packing(monkeypatch):
    monkeypatch.setattr(sys, 'byteorder', 'big')

    buffer = pack('i', 42)
    data, = unpack('i', buffer)
    assert data == 42


def test_default_filename():
    assert brand_filename('file') == 'file.comp'
