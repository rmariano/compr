import pytest

from compressor.char_node import CharNode


def test_charnode_eq():
    assert CharNode("first", 1) == CharNode("second", 1)


def test_charnode_lt():
    assert CharNode("smaller", 1) < CharNode("bigger", 2)


def test_charnode_is_leaf():
    assert CharNode("leaf", 1).leaf is True


def test_charnode_is_not_leaf():
    left = CharNode("left", 1)
    right = CharNode("right", 1)
    root = CharNode("root", 1, left, right)
    assert root.leaf is False


def test_merge_nodes():
    left_char = CharNode("A", 13)
    right_char = CharNode("B", 27)

    new_node = left_char + right_char

    assert new_node.value == "AB"
    assert new_node.freq == left_char.freq + right_char.freq
    assert new_node.left is left_char
    assert new_node.right is right_char


def test_merge_invalid_nodes():
    with pytest.raises(TypeError):
        CharNode("A", 1) + "B"
