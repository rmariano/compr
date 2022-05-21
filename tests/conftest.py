"""Base for all tests with definitions of fixtures"""
import glob
import os

from compressor.util import open_text_file

TEST_DATA_FILES_LOCATION = os.path.join(os.path.dirname(__file__), "data")
TEST_DATA_FILES = glob.glob(os.path.join(TEST_DATA_FILES_LOCATION, "*.txt"))
DATA_FILES_FIXTURE_NAME = "data_file"


def _load_files_contents(*files):
    for file_ in files:
        with open_text_file(file_) as source:
            yield source.read()


def pytest_generate_tests(metafunc):
    """All tests that take a fixture named ``data_file`` will be parameterized
    with all the testing data files.

    This means, the test can be made to work with a single test file as an
    input, but instead it will run once per every file present in the directory
    ``TEST_DATA_FILES_LOCATION``.
    """
    if DATA_FILES_FIXTURE_NAME in metafunc.fixturenames:
        metafunc.parametrize(
            DATA_FILES_FIXTURE_NAME,
            _load_files_contents(*TEST_DATA_FILES),
            ids=TEST_DATA_FILES,
        )
