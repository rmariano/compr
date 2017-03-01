from compressor.core import CharNode


def test_charnode_eq():
    assert CharNode('first', 1) == CharNode('second', 1)


def test_charnode_lt():
    assert CharNode('smaller', 1) < CharNode('bigger', 2)


def test_charnode_is_leaf():
    assert CharNode('leaf', 1).leaf is True


def test_charnode_is_not_leaf():
    left = CharNode('left', 1)
    right = CharNode('right', 1)
    root = CharNode('root', 1, left, right)
    assert root.leaf is False
