"""
Compressor CLI (command-line interface) module.
Exposes the entry point to the program for executing as command line.
"""
import argparse
import sys

from compressor.constants import VERSION
from compressor.pycompressor import PyCompressor


def argument_parser() -> argparse.ArgumentParser:
    """Create the argument parser object to be used for parsing the arguments
    from sys.argv
    """
    parser = argparse.ArgumentParser(
        prog="PyCompress", description="Compress text files."
    )
    parser.add_argument(
        "filename", type=str, help="Name of the file to process"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-c", "--compress", action="store_true", help="Compress the file"
    )
    group.add_argument(
        "-x", "--extract", action="store_true", help="Extract the file"
    )
    parser.add_argument(
        "-d",
        "--dest-file",
        type=str,
        default=None,
        help="Destination File Name",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=VERSION),
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


def main() -> int:  # pragma: nocover
    """Program cli

    :return: Status code of the program.
    :rtype: int
    """
    return PyCompressor(**parse_arguments()).run()


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
