import glob
import os
import subprocess
import tempfile
from tests import BaseTest
from compressor.main import main


def _files_identical(*files):
    """Check if the list of provided files are identical.
    returns :bool:"""
    if not files:
        raise ValueError("No files provided for comparison")
    hashes = {subprocess.check_output(['sha256sum', fn]).split()[0] for fn in files}
    return len(hashes) == 1


class SmokeTest(BaseTest):
    """Test that a reconstructed file (a file that was decompressed from
    a previous compression process) is identical to the original."""

    def test_compress_and_retrieve_datasets(self):
        """Content must be unmodified, meaning the extracted file must exactly
        match the content prior compression."""
        for source in glob.glob(os.path.join(self.store, '*.txt')):
            target = tempfile.NamedTemporaryFile().name
            # Compress
            main(source, compress=True, dest_file=target)
            # Now extract
            extracted = tempfile.NamedTemporaryFile().name
            main(target, extract=True, compress=False, dest_file=extracted)
            self.assertTrue(_files_identical(source, extracted), source)


if __name__ == '__main__':
    unittest.main()
