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
    t = create_tree_code(freqs)
    table = parse_tree_code(t)
    #print("Original:\n {}".format(table))
    save_compressed_file(filename, table)
    retrieve_compressed_file(filename)



if __name__ == '__main__':
    compress(sys.argv[1])
