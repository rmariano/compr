import heapq
import struct
from collections import Counter

ENC = 'utf-8'


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


def save_table(dest_file, table):
    """Store the table in the destination file.
    c: char
    L: code of c (unsigned Long)"""
    content = None  # of the file
    offset = len(table)
    tokens = [(bytes(char, encoding=ENC), v) for char, v in table.items()]
    content = struct.pack('i', offset)
    content += struct.pack('{}c'.format(offset), *[t[0] for t in tokens])
    content += struct.pack('{}L'.format(offset), *[int(t[1], base=2) for t in tokens])
    dest_file.write(content)


def _sizeof(code):
    sizes = {'i': 4, 'c': 1, 'L': 4}
    return sizes.get(code, 1)


def retrieve_table(dest_file):
    """Read the binary file, and return the translation table as a reversed
    dict."""
    offset, *_ = struct.unpack('i', dest_file.read(_sizeof('i')))
    chars = dest_file.read(offset * _sizeof('c'))
    codes = dest_file.read(offset * _sizeof('L'))
    chars = struct.unpack('{}c'.format(offset), chars)
    codes = struct.unpack('{}L'.format(offset), codes)
    return {bin(code): str(char, encoding=ENC) for char, code in zip(chars, codes)}


def _brand_filename(filename):
    return "{}.comp".format(filename)


def save_compressed_file(filename, table):
    """Given the original file by its <filename>, save a new one.
    <table> contains the new codes for each character on <filename>"""
    new_file = _brand_filename(filename)
    with open(new_file, 'wb') as f:
        save_table(f, table)


def retrieve_compressed_file(filename):
    """Reconstruct the original file from the compressed copy."""
    fname = _brand_filename(filename)
    with open(fname, 'rb') as f:
        t = retrieve_table(f)
        #print("Retrieved table:\n{}".format(t))
