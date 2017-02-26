"""Tests for the set of functions defined in compressor.functions"""
import sys

from compressor.functions import endianess_prefix


def test_endianess_prefix_bigendinan(monkeypatch):
    monkeypatch.setattr(sys, 'byteorder', 'big')
    assert endianess_prefix() == '>'


def test_endianess_prefix_bytes(monkeypatch):
    monkeypatch.setattr(sys, 'byteorder', 'big')
    assert endianess_prefix(bytes) == b'>'
