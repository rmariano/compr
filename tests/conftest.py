import os
import glob
import pytest


@pytest.fixture
def data_store():
    return os.path.join(os.path.dirname(__file__), 'data')


@pytest.fixture
def data_files(data_store):
    """Stream all file names on the test data directory, to be used on tests"""
    yield from glob.glob(os.path.join(data_store, '*.txt'))
