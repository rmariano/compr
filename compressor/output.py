"""Logic associated with the output (destination or target) files."""
from pathlib import Path

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
        self._original_filename: Path = Path(original_filename)
        self.default_extension: str = self.DEFAULT_EXTENSIONS[action]
        self._destination_filename: Path = Path(
            destination_filename or
            default_filename(original_filename, suffix=self.default_extension)
        )
        self._output_dir: Path = None
        if output_dir is not None:
            self._output_dir = Path(output_dir)

    def _under_directory(self) -> Path:
        if self._output_dir is None:
            return self._destination_filename
        return self._output_dir / self._destination_filename.name

    @property
    def value(self) -> str:
        return str(self._under_directory())
