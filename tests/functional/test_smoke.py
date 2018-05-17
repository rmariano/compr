import hashlib
import subprocess
import tempfile
from typing import List

import pytest

from compressor.cli import PyCompressor
from tests.conftest import data_files, data_store


def _all_files_identical(*files: List[str]) -> bool:
    """Check if the list of provided files are identical.
    returns :bool:
    """
    hashes = set()
    for filename in files:
        with open(filename, 'rb') as fname:
            content = fname.read()
            hashed = hashlib.sha256(content).hexdigest()
            hashes.add(hashed)
    return len(hashes) == 1


@pytest.mark.parametrize('source', data_files(data_store()))
def test_compress_and_retrieve_datasets(source):
    """Content must be unmodified, meaning the extracted file must
    match the content prior compression.
    """
    target = tempfile.NamedTemporaryFile().name
    # Compress
    PyCompressor(source, compress=True, dest_file=target).run()
    # Now extract
    extracted = tempfile.NamedTemporaryFile().name
    PyCompressor(target, extract=True, compress=False,
                 dest_file=extracted).run()
    assert _all_files_identical(source, extracted)


def test_cli_invocation():
    """The entry point works"""
    st_code = subprocess.check_call(('pycompress', '-h'))
    assert st_code == 0
