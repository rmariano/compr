import random
import os
from tests import BaseTest
from compressor.core import process_frequencies


class TestCore(BaseTest):
    """Unit tests in the core functions."""

    def test_stream_counter_data(self):
        """Check that the function that processes the frequencies, computes
        correctly."""
        print(self.store)
        with open(os.path.join(self.store, 'test001.txt'), 'r') as f:
            result = process_frequencies(f.read())
        expected = {'a': 45, 'b': 13, 'c': 11, 'd': 16, 'e': 9, 'f': 5, '\n': 1}
        for node in result:
            self.assertEqual(node.freq, expected[node.value])

    def test_stream_counter_randomized(self):
        """Generate a random string, and test the process_frequencies
        function."""
        selected_chars = ('a', 'Z', 'e', 'g', 'd', 's', 't', 'm', 'r', 'l')
        stream = ''
        expected = {k: 0 for k in selected_chars}
        for _ in range(100):
            multiplier = random.randint(1, 100)
            char = random.choice(selected_chars)
            stream += char * multiplier
            expected[char] += multiplier
        result = process_frequencies(stream)
        for node in result:
            self.assertEqual(node.freq, expected[node.value])


if __name__ == '__main__':
    unittest.main()
