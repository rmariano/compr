import hashlib
import subprocess
import tempfile
from itertools import groupby
from typing import List

import pytest

from compressor.cli import main_engine
from tests.conftest import data_files, data_store


def _all_equal(iterable):
    group = groupby(iterable)
    return next(group, True) and not next(group, False)


def _all_file_hashes(*files: List[str]):
    for filename in files:
        with open(filename, "rb") as fname:
            content = fname.read()
            yield hashlib.sha256(content).hexdigest()


def _all_files_identical(*files: List[str]) -> bool:
    """Check if the list of provided files are identical.
    returns :bool:
    """
    return _all_equal(_all_file_hashes(*files))


@pytest.mark.parametrize("source", data_files(data_store()))
def test_compress_and_retrieve_datasets(source):
    """Content must be unmodified, meaning the extracted file must
    match the content prior compression.
    """
    target = tempfile.NamedTemporaryFile().name
    # Compress
    main_engine(source, compress=True, dest_file=target)
    # Now extract
    extracted = tempfile.NamedTemporaryFile().name
    main_engine(target, extract=True, compress=False, dest_file=extracted)
    assert _all_files_identical(source, extracted)


def test_cli_invocation():
    """The entry point works"""
    st_code = subprocess.check_call(("pycompress", "-h"))
    assert st_code == 0
