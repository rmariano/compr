import sys
from core import (
    process_frequencies,
    create_tree_code,
    parse_tree_code,
    save_compressed_file,
    retrieve_compressed_file,
)


def main():
    pass


def compress(filename):
    with open(filename, 'r') as f:
        freqs = process_frequencies(f.read())
    checksum = sum(c.freq for c in freqs)  # bytes
    t = create_tree_code(freqs)
    table = parse_tree_code(t)
    save_compressed_file(filename, table, checksum)


def extract(filename):
    retrieve_compressed_file(filename)


if __name__ == '__main__':
    compress(sys.argv[1])
