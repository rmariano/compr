import unittest
import os


class BaseTest(unittest.TestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.store = os.path.join(os.path.dirname(__file__), 'data')
