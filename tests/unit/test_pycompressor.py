import pytest

from compressor.pycompressor import PyCompressor


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
