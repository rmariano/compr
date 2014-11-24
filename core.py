import heapq
from collections import Counter


class CharNode(object):

    def __init__(self, value, freq, left=None, right=None):
        self.value = value
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

    def __le__(self, other):
        return self.freq <= other.freq

    def __gt__(self, other):
        return self.freq > other.freq

    def __ge__(self, other):
        return self.freq >= other.freq

    def __eq__(self, other):
        return self.freq == other.freq

    def __ne__(self, other):
        return self.freq != other.freq

    @property
    def leaf(self):
        return self.left is None and self.right is None


def create_tree_code(C):
    """Receives a :list: of :CharNode: (characters) C,
    namely leaves in the tree, and returns a tree with the corresponding
    prefix-free code."""
    n = len(C)
    Q = C
    heapq.heapify(Q)
    for _ in range(1, n):
        z = CharNode('', 0)
        z.left = x = heapq.heappop(Q)
        z.right = y = heapq.heappop(Q)
        z.freq = x.freq + y.freq
        heapq.heappush(Q, z)
    return heapq.heappop(Q)


def parse_tree_code(tree, table=None, code=b''):
    """Given the tree with the chars-frequency processed, return a table that
    maps each character with its binary representation on the new code:
    left --> 0
    right --> 1
    """
    table = table or {}
    LEFT = b'0'
    RIGHT = b'1'
    if tree.leaf:
        table[tree.value] = code
        return table
    table.update(parse_tree_code(tree.left, table, code+LEFT))
    table.update(parse_tree_code(tree.right, table, code+RIGHT))
    return table


def process_frequencies(stream):
    """Given a stream of text, return a list of CharNode with the frequencies
    for each character."""
    counts = Counter(stream)
    return [CharNode(value=value, freq=freq) for value, freq in counts.items()]

