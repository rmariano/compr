"""
Compressor main module.
Exposes the entry point to the program for executing as command line,
as well as the main functions to be used as library.
This module contains high-level functionality.
"""
import argparse
import sys
from .core import (
    process_frequencies,
    create_tree_code,
    parse_tree_code,
    save_compressed_file,
    retrieve_compressed_file,
)
from compressor.constants import VERSION


def compress_file(filename: str, dest_file: str=None) -> None:
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


def extract_file(filename: str, dest_file: str=None) -> None:
    """
    Extract the compressed <filename> into <dest_file>

    :param filename:  Name of the file to open for extraction.
    :param dest_file: Name (path) where to dump the result.
    """
    retrieve_compressed_file(filename, dest_file)


def argument_parser() -> argparse.ArgumentParser:
    """Create the argument parser object to be used for parsing the arguments
    from sys.argv
    """
    parser = argparse.ArgumentParser(
        prog='PyCompress',
        description="Compress text files.",
    )
    parser.add_argument(
        'filename',
        type=str,
        help="Name of the file to process"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-c', '--compress',
        action='store_true',
        help="Compress the file"
    )
    group.add_argument(
        '-x', '--extract',
        action='store_true',
        help="Extract the file"
    )
    parser.add_argument(
        '-d', '--dest-file',
        type=str,
        default=None,
        help="Destination File Name"
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s {version}'.format(version=VERSION)
    )
    return parser


def parse_arguments(args=None) -> dict:
    """Parse the command-line (cli) provided arguments, and return a mapping of
    the options selected by the user with their values.

    :return: dict with the kwargs provided in cli
    """
    parser = argument_parser()
    args = parser.parse_args(args)
    return vars(args)


def main_engine(filename: str, extract: bool=False,
                compress: bool=True, dest_file=None) -> int:
    """
    Main functionality for the program cli or call as library.
    `extract` & `compress` must have opposite values.

    :param filename:  Path to the source file to process.
    :param extract:   If True, sets the program for a extraction.
    :param compress:  If True, the program should compress a file.
    :param dest_file: Optional name of the target file.

    :return: 0 if executed without problems.
    """
    assert extract is not compress, "Cannot both extract & compress"
    if compress:
        compress_file(filename, dest_file)
    if extract:
        extract_file(filename, dest_file)
    return 0


def main() -> int:
    """
    Program cli

    :return: Status code of the program.
    :rtype: int
    """
    return main_engine(**parse_arguments())


if __name__ == '__main__':
    sys.exit(main())
