"""Unit tests the core functions"""
import pytest
import os
import random

from compressor.core import (create_tree_code, parse_tree_code,
                             process_frequencies)
from tests.conftest import data_files, data_store


def test_stream_counter_data(data_store):
    """The function that processes the frequencies correctly."""
    with open(os.path.join(data_store, 'test001.txt'), 'r') as f:
        result = process_frequencies(f.read())

    mapped_result = {node.value: node.freq for node in result}
    expected = {'a': 45, 'b': 13, 'c': 11, 'd': 16, 'e': 9, 'f': 5, '\n': 1}

    assert mapped_result == expected


def test_stream_counter_randomized():
    selected_chars = ('a', 'Z', 'e', 'g', 'd', 's', 't', 'm', 'r', 'l')
    stream = ''
    expected = {k: 0 for k in selected_chars}
    for _ in range(100):
        multiplier = random.randint(1, 100)
        char = random.choice(selected_chars)
        stream += char * multiplier
        expected[char] += multiplier

    result = process_frequencies(stream)
    mapped_result = {node.value: node.freq for node in result}
    assert mapped_result == expected


@pytest.mark.parametrize('source', data_files(data_store()))
def test_preffix_free(source):
    """The internal table generates new variable-length prefix-free code."""
    with open(source, 'r') as f:
        freqs = process_frequencies(f.read())

    checksum = sum(c.freq for c in freqs)  # bytes
    t = create_tree_code(freqs)
    table = parse_tree_code(t)
    codes = sorted(table.values(), key=lambda x: (len(x), x))
    current_code = codes.pop(0)
    while codes:
        for code in codes:
            assert not code.startswith(current_code), \
                    "{} is prefix of {}".format(current_code, code)
        current_code = codes.pop(0)
