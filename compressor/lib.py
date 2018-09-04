"""compressor.lib

High-level functions exposed as a library, that can be imported.
"""
from compressor.core import retrieve_compressed_file as extract_file  # pylint: disable=unused-import
from compressor.core import (create_tree_code, parse_tree_code,
                             process_frequencies, save_compressed_file)


def compress_file(filename: str, dest_file: str = "") -> None:
    """
    Open the <filename> and compress its contents on a new one.

    :param filename:  The path to the source file to compress.
    :param dest_file: The name of the target file. If not provided (None),
                      a default will be used with `<filename>.comp`
    """
    with open(filename, 'r') as source:
        freqs = process_frequencies(source.read())

    checksum = sum(c.freq for c in freqs)  # bytes
    tree_code = create_tree_code(freqs)
    table = parse_tree_code(tree_code)
    save_compressed_file(filename, table, checksum, dest_file)
