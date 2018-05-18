"""Logic associated with the output (destination or target) files."""
import os

from compressor.functions import default_filename
from compressor.constants import Actions


class OutputFileName:
    """Resolve the final name of the file to write the bytes to."""
    DEFAULT_EXTENSIONS = {Actions.COMPRESS: "comp", Actions.EXTRACT: "extr"}

    def __init__(
        self,
        original_filename: str,
        action: Actions,
        destination_filename: str = None,
        output_dir: str = None,
    ):
        self._original_filename = original_filename
        self.default_extension = self.DEFAULT_EXTENSIONS[action]
        self._destination_filename = destination_filename
        self._output_dir = output_dir

    def _final_output_filename(self):
        """Only the file name, without being prefixed by the directory."""
        return self._destination_filename or default_filename(
            self._original_filename, suffix=self.default_extension
        )

    def _prefix_directory(self, output_filename) -> str:
        if self._output_dir is None:
            return output_filename

        filename = os.path.basename(output_filename)
        return os.path.join(self._output_dir, filename)

    @property
    def value(self):
        output_filename_so_far = self._final_output_filename()
        return self._prefix_directory(output_filename_so_far)
