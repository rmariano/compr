"""Base for all tests with common objects, helpers, and utils.
"""
import unittest
import os


class BaseTest(unittest.TestCase):
    """Define basic setup functions for the rest of the tests.
    Specific tests should call the kook with super().setUp()
    """

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.store = os.path.join(os.path.dirname(__file__), 'data')
