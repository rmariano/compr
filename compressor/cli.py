"""
Compressor CLI (command-line interface) module.
Exposes the entry point to the program for executing as command line.
"""
import argparse
import sys

from compressor.constants import VERSION, Actions
from compressor.lib import compress_file, extract_file
from compressor.output import OutputFileName


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


class PyCompressor:
    """Work as an orchestrator for the actions to be dispatched, based on the
    parameters provided.

    Interpret the parameters, and run the corresponding actions.
    """
    ACTION_OPERATIONS = {
        Actions.COMPRESS: compress_file,
        Actions.EXTRACT: extract_file,
    }

    def __init__(
        self,
        filename: str,
        extract: bool = False,
        compress: bool = True,
        dest_file: str = None,
        output_dir: str = None,
    ):
        """
        :param filename:  Path to the source file to process.
        :param extract:   If True, sets the program for a extraction.
        :param compress:  If True, the program should compress a file.
        :param dest_file: Optional name of the target file.
        """
        self._filename = filename
        self._action = Actions.from_flags(compress, extract)
        self.destination = OutputFileName(
            filename, self._action, dest_file, output_dir
        ).value

    def run(self) -> int:
        operation = self.ACTION_OPERATIONS[self._action]
        operation(self._filename, self.destination)
        return 0


def main() -> int:  # pragma: nocover
    """Program cli

    :return: Status code of the program.
    :rtype: int
    """
    return PyCompressor(**parse_arguments()).run()


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
