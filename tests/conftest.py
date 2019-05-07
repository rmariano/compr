"""Base for all tests with definitions of fixtures"""
import glob
import os

TEST_DATA_FILES_LOCATION = os.path.join(os.path.dirname(__file__), "data")
TEST_DATA_FILES = glob.glob(os.path.join(TEST_DATA_FILES_LOCATION, "*.txt"))
DATA_FILES_FIXTURE_NAME = "data_file"


def _load_files_contents(*files):
    for file_ in files:
        with open(file_) as source:
            yield source.read()


def pytest_generate_tests(metafunc):  # pylint: disable=C0111
    if DATA_FILES_FIXTURE_NAME in metafunc.fixturenames:
        metafunc.parametrize(
            DATA_FILES_FIXTURE_NAME,
            _load_files_contents(*TEST_DATA_FILES),
            ids=TEST_DATA_FILES,
        )
