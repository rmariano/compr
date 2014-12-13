import sys
import argparse
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


def parse_arguments():
    parser = argparse.ArgumentParser(description="Compress text files.")
    parser.add_argument('file', type=str,
                        help="Name of the file to process")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--compress', action='store_true',
                       help="Compress the file")
    group.add_argument('-x', '--extract', action='store_true',
                       help="Extract the file")
    args = parser.parse_args()
    return vars(args)


if __name__ == '__main__':
    compress(sys.argv[1])
