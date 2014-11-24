import sys
from core import (
    process_frequencies,
    create_tree_code,
    parse_tree_code,
)


def main():
    pass


def compress(filename):
    with open(filename, 'r') as f:
        freqs = process_frequencies(f.read())
    t = create_tree_code(freqs)
    d = parse_tree_code(t)
    print(d)


if __name__ == '__main__':
    compress(sys.argv[1])
