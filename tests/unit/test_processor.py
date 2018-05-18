"""Unit tests the core functions"""
import os
from collections import Counter, deque

import pytest

from compressor.core import (
    create_tree_code,
    parse_tree_code,
    process_frequencies,
)
from tests.conftest import data_files, data_store


def test_stream_counter_data(data_store):
    """The function that processes the frequencies correctly."""
    with open(os.path.join(data_store, "test001.txt"), "r") as f:
        result = process_frequencies(f.read())

    mapped_result = {node.value: node.freq for node in result}
    expected = {"a": 45, "b": 13, "c": 11, "d": 16, "e": 9, "f": 5, "\n": 1}

    assert mapped_result == expected


@pytest.mark.parametrize("source", data_files(data_store()))
def test_frequencies_add_up(source):
    with open(source, "r") as f:
        content = f.read()

    frequencies = process_frequencies(content)
    checksum = sum(c.freq for c in frequencies)
    expected = sum(Counter(content).values())

    assert checksum == expected


@pytest.mark.parametrize("source", data_files(data_store()))
def test_preffix_free(source):
    """The internal table generates new variable-length prefix-free code."""
    with open(source, "r") as f:
        freqs = process_frequencies(f.read())

    t = create_tree_code(freqs)
    table = parse_tree_code(t)

    codes = deque(table.values())
    for code_to_check in codes:
        prefix = {c for c in codes if c.startswith(code_to_check)}
        assert prefix == {code_to_check}
