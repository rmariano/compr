"""Tests for the command line arguments"""
from argparse import Namespace

import pytest

from compressor.cli import argument_parser, parse_arguments, PyCompressor
from compressor.constants import VERSION


@pytest.fixture
def argparser():
    return argument_parser()


@pytest.mark.parametrize("opt", ("-c", "--compress"))
def test_compress(argparser, opt):
    to_compress = argparser.parse_args([opt, "foo"])
    expected = Namespace(
        filename="foo", compress=True, extract=False, dest_file=None
    )
    assert to_compress == expected


@pytest.mark.parametrize("opt", ("-x", "--extract"))
def test_extract(argparser, opt):
    tbe = argparser.parse_args((opt, "foo"))
    expected = Namespace(
        filename="foo", extract=True, compress=False, dest_file=None
    )
    assert tbe == expected


def test_cannot_both_compress_and_extract(argparser):
    with pytest.raises(SystemExit):
        argparser.parse_args(("-x", "-c", "foo"))
        argparser.parse_args("--extract", "--compress", "bar")


def test_version(argparser):
    with pytest.raises(SystemExit):
        version = argparser.parse_args(("--version",))
        assert version == "PyCompress {0}".format(VERSION)


@pytest.mark.parametrize("opt", ("-x", "--extract", "-c", "--compress"))
def test_output_name(argparser, opt):
    command = argparser.parse_args((opt, "-d", "foo", "bar"))
    assert command.dest_file == "foo"
    assert command.filename == "bar"
    assert (command.compress ^ command.extract) is True


@pytest.mark.parametrize("opt", ("-c", "--compress"))
def test_parse_compress_as_dict(opt):
    result = parse_arguments((opt, "foo"))
    expected = {
        "compress": True,
        "extract": False,
        "dest_file": None,
        "filename": "foo",
    }
    assert result == expected


@pytest.mark.parametrize("opt", ("-x", "--extract"))
def test_parse_extract_as_dict(opt):
    result = parse_arguments((opt, "foo"))
    expected = {
        "compress": False,
        "extract": True,
        "dest_file": None,
        "filename": "foo",
    }
    assert result == expected


def test_parse_with_filename_as_dict():
    result = parse_arguments(("-x", "-d", "foo", "bar"))
    expected = {
        "compress": False,
        "extract": True,
        "dest_file": "foo",
        "filename": "bar",
    }
    assert result == expected


def test_pycompressor_default_filename_compression():
    app = PyCompressor("filename", extract=False, compress=True)
    assert app.destination == "filename.comp"


def test_pycompressor_default_filename_extraction():
    app = PyCompressor("filename", extract=True, compress=False)
    assert app.destination == "filename.extr"


@pytest.mark.parametrize("extract,compress", ((True, False), (False, True)))
def test_pycompressor_filename_provided(extract, compress):
    app = PyCompressor(
        "source-filename",
        extract=extract,
        compress=compress,
        dest_file="something-custom",
    )
    assert app.destination == "something-custom"


@pytest.mark.parametrize(
    "extract,compress,expected",
    ((True, False, "output/source.extr"), (False, True, "output/source.comp")),
)
def test_pycompressor_default_and_output_dir(extract, compress, expected):
    app = PyCompressor(
        "source", extract=extract, compress=compress, output_dir="output/"
    )
    assert app.destination == expected


@pytest.mark.parametrize(
    "extract,compress,output,expected",
    (
        (True, False, "output/", "output/destination"),
        (False, True, "output/", "output/destination"),
        (True, False, "some-dir", "some-dir/destination"),
    ),
)
def test_pycompressor_destination_and_output_dir(
    extract, compress, output, expected
):
    app = PyCompressor(
        "source",
        extract=extract,
        compress=compress,
        dest_file="destination",
        output_dir=output,
    )
    assert app.destination == expected
