"""Tests for the command line arguments"""
from argparse import Namespace

import pytest

from compressor import argument_parser, parse_arguments
from compressor.constants import VERSION


@pytest.fixture
def argparser():
    return argument_parser()


@pytest.mark.parametrize('opt', ('-c', '--compress'))
def test_compress(argparser, opt):
    to_compress = argparser.parse_args([opt, 'foo'])
    expected = Namespace(filename='foo', compress=True,
                         extract=False, dest_file=None)
    assert to_compress == expected


@pytest.mark.parametrize('opt', ('-x', '--extract'))
def test_extract(argparser, opt):
    tbe = argparser.parse_args((opt, 'foo'))
    expected = Namespace(filename='foo', extract=True,
                         compress=False, dest_file=None)
    assert tbe == expected


def test_cannot_both_compress_and_extract(argparser):
    with pytest.raises(SystemExit):
        argparser.parse_args(('-x', '-c', 'foo'))
        argparser.parse_args('--extract', '--compress', 'bar')


def test_version(argparser):
    with pytest.raises(SystemExit):
        version = argparser.parse_args(('--version', ))
        assert version == "PyCompress {0}".format(VERSION)


@pytest.mark.parametrize('opt', ('-x', '--extract', '-c', '--compress'))
def test_output_name(argparser, opt):
    command = argparser.parse_args((opt, '-d', 'foo', 'bar'))
    assert command.dest_file == 'foo'
    assert command.filename == 'bar'
    assert (command.compress ^ command.extract) is True


@pytest.mark.parametrize('opt', ('-c', '--compress'))
def test_parse_compress_as_dict(opt):
    result = parse_arguments((opt, 'foo'))
    expected = {
        'compress': True,
        'extract': False,
        'dest_file': None,
        'filename': 'foo',
    }
    assert result == expected


@pytest.mark.parametrize('opt', ('-x', '--extract'))
def test_parse_extract_as_dict(opt):
    result = parse_arguments((opt, 'foo'))
    expected = {
        'compress': False,
        'extract': True,
        'dest_file': None,
        'filename': 'foo',
    }
    assert result == expected


def test_parse_with_filename_as_dict():
    result = parse_arguments(('-x', '-d', 'foo', 'bar'))
    expected = {
        'compress': False,
        'extract': True,
        'dest_file': 'foo',
        'filename': 'bar',
    }
    assert result == expected
