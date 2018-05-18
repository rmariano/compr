"""Base for all tests with definitions of fixtures"""
import glob
import os

import pytest


@pytest.fixture
def data_store():
    """Path where the data files are located"""
    return os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture
def data_files(data_store):  # pylint: disable=redefined-outer-name
    """Stream all file names on the test data directory, to be used on tests"""
    yield from glob.glob(os.path.join(data_store, "*.txt"))
