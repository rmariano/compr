"""
Compressor CLI (command-line interface) module.
Exposes the entry point to the program for executing as command line.
"""
import argparse
import sys
import os

from compressor.constants import VERSION
from compressor.lib import compress_file, extract_file
from compressor.functions import default_filename


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
        self._extract = extract
        self._compress = compress
        self._dest_file = dest_file
        self._output_dir = output_dir

    def _default_extension_for_action(self) -> str:
        if self._compress:
            return "comp"
        elif self._extract:
            return "extr"
        assert False, "Unknown action"

    @property
    def destination_file(self):
        return self._dest_file or default_filename(
            self._filename, self._default_extension_for_action()
        )

    def _prefix_directory(self) -> str:
        if self._output_dir is None:
            return self.destination_file
        filename = os.path.basename(self.destination_file)
        return os.path.join(self._output_dir, filename)

    @property
    def destination(self) -> str:
        """Compute the destination where the output file is to be written."""
        return self._prefix_directory()

    def run(self) -> int:
        if self._compress:
            compress_file(self._filename, self.destination)
        if self._extract:
            extract_file(self._filename, self.destination)
        return 0


def main() -> int:  # pragma: nocover
    """Program cli

    :return: Status code of the program.
    :rtype: int
    """
    return PyCompressor(**parse_arguments()).run()


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
