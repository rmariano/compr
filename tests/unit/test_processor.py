"""Unit tests the core functions"""
from collections import Counter, deque

from compressor.core import (
    create_tree_code,
    parse_tree_code,
    process_frequencies,
)


def test_stream_counter_data(data_file):
    """The function that processes the frequencies correctly."""
    freq_processed = process_frequencies(data_file)
    mapped_result = {node.value: node.freq for node in freq_processed}
    expected = Counter(data_file)

    assert mapped_result == expected


def test_frequencies_add_up(data_file):
    frequencies = process_frequencies(data_file)
    checksum = sum(c.freq for c in frequencies)
    expected = sum(Counter(data_file).values())

    assert checksum == expected


def test_preffix_free(data_file):
    """The internal table generates new variable-length prefix-free code."""
    freqs = process_frequencies(data_file)
    t = create_tree_code(freqs)
    table = parse_tree_code(t)

    codes = deque(table.values())
    for code_to_check in codes:
        prefix = {c for c in codes if c.startswith(code_to_check)}
        assert prefix == {code_to_check}
