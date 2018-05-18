from compressor.constants import Actions


def test_compress_action():
    assert Actions.from_flags(True, False) == Actions.COMPRESS


def test_extract_action():
    assert Actions.from_flags(False, True) == Actions.EXTRACT
