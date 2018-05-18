"""Testt that the output file is computed correctly."""
import pytest

from compressor.constants import Actions
from compressor.output import OutputFileName


def test_default_filename_compression():
    out = OutputFileName("filename", action=Actions.COMPRESS).value
    assert out == "filename.comp"


def test_default_filename_extraction():
    out = OutputFileName("filename", action=Actions.EXTRACT).value
    assert out == "filename.extr"


@pytest.mark.parametrize("action", (Actions.EXTRACT, Actions.COMPRESS))
def test_pycompressor_filename_provided(action):
    out = OutputFileName(
        "source-filename",
        action=action,
        destination_filename="something-custom",
    )
    assert out.value == "something-custom"


@pytest.mark.parametrize(
    "action,expected",
    (
        (Actions.EXTRACT, "output/source.extr"),
        (Actions.COMPRESS, "output/source.comp"),
    ),
)
def test_pycompressor_default_and_output_dir(action, expected):
    out = OutputFileName("source", action, output_dir="output/").value
    assert out == expected


@pytest.mark.parametrize(
    "action,output,expected",
    (
        (Actions.EXTRACT, "output/", "output/destination"),
        (Actions.COMPRESS, "output/", "output/destination"),
        (Actions.EXTRACT, "some-dir", "some-dir/destination"),
    ),
)
def test_pycompressor_destination_and_output_dir(action, output, expected):
    out = OutputFileName(
        "source",
        action=action,
        destination_filename="destination",
        output_dir=output,
    )
    assert out.value == expected
