from unittest import mock

from compressor.constants import Actions
from compressor.pycompressor import PyCompressor


def test_pycompressor_extract_called():
    extract_file = mock.Mock()
    new_action = {Actions.EXTRACT: extract_file}
    with mock.patch.object(PyCompressor, "ACTION_OPERATIONS", new=new_action):
        PyCompressor(
            "source", extract=True, compress=False, dest_file="output"
        ).run()
    extract_file.assert_called_with("source", "output")


def test_pycompressor_compress_called():
    compress_file = mock.Mock()
    new_action = {Actions.COMPRESS: compress_file}
    with mock.patch.object(PyCompressor, "ACTION_OPERATIONS", new=new_action):
        PyCompressor(
            "source", extract=False, compress=True, dest_file="output"
        ).run()
    compress_file.assert_called_with("source", "output")
