import glob
import random
import os
from tests import BaseTest
from compressor.core import (
    process_frequencies,
    create_tree_code,
    parse_tree_code,
)


class TestCore(BaseTest):
    """Unit tests in the core functions."""

    def test_stream_counter_data(self):
        """Check that the function that processes the frequencies, computes
        correctly."""
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

    def test_preffix_free(self):
        """Assert that the internal table generates new variable-length
        prefix-free code."""
        for source in glob.glob(os.path.join(self.store, '*.txt')):
            with open(source, 'r') as f:
                freqs = process_frequencies(f.read())
            checksum = sum(c.freq for c in freqs)  # bytes
            t = create_tree_code(freqs)
            table = parse_tree_code(t)
            codes = sorted(table.values(), key=lambda x: (len(x), x))
            current_code = codes.pop(0)
            while codes:
                for code in codes:
                    self.assertFalse(code.startswith(current_code),
                                     "{} is prefix of {}".format(current_code, code))
                current_code = codes.pop(0)


if __name__ == '__main__':
    unittest.main()
