"""Main Logic Object"""
from compressor.constants import Actions
from compressor.lib import compress_file, extract_file
from compressor.output import OutputFileName


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
