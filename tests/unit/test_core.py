"""Tests for `compressor.core`."""

import itertools
import operator

from compressor.core import CharNode, process_frequencies


def test_charnode_hashable():
    """A CharNode can be used in sets."""
    assert len({CharNode("hello", 42), CharNode("hello", 42)}) == 1


def test_process_frequencies():
    """The right nodes are in the list."""
    expected = {l: i for i, l in enumerate(("a", "b", "c", "d", "e"), start=1)}
    stream = "".join(itertools.starmap(operator.mul, expected.items()))
    freqs = set(process_frequencies(stream))

    assert freqs == {CharNode(l, f) for l, f in expected.items()}


def test_process_empty_frequencies():
    """For '' ->  []."""
    assert process_frequencies("") == []
