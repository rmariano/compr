import glob
import hashlib
import os
import subprocess
import tempfile
from typing import List

from compressor import main_engine
from tests import BaseTest


def _all_files_identical(*files: List[str]) -> bool:
    """Check if the list of provided files are identical.
    returns :bool:
    """
    hashes = set()
    for filename in files:
        with open(filename, 'rb') as fname:
            content = fname.read()
            hashed = hashlib.sha256(content).hexdigest()
            hashes.add(hashed)
    return len(hashes) == 1


class SmokeTest(BaseTest):
    """Test that a reconstructed file (a file that was decompressed from
    a previous compression process) is identical to the original.
    """

    def test_compress_and_retrieve_datasets(self):
        """Content must be unmodified, meaning the extracted file must
        match the content prior compression.
        """
        for source in glob.glob(os.path.join(self.store, '*.txt')):
            target = tempfile.NamedTemporaryFile().name
            # Compress
            main_engine(source, compress=True, dest_file=target)
            # Now extract
            extracted = tempfile.NamedTemporaryFile().name
            main_engine(target, extract=True, compress=False, dest_file=extracted)
            self.assertTrue(_all_files_identical(source, extracted), source)


if __name__ == '__main__':
    unittest.main()
