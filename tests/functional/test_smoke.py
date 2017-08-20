import hashlib
import tempfile
import pytest
from typing import List

from compressor.cli import main_engine
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
    main_engine(source, compress=True, dest_file=target)
    # Now extract
    extracted = tempfile.NamedTemporaryFile().name
    main_engine(target, extract=True, compress=False, dest_file=extracted)
    assert _all_files_identical(source, extracted)
