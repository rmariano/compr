"""Constant definitions are defined here, and imported everywhere else in the
code.

This should contain definitions for values that do not change while the program
is running, and are to remain constant throughout the execution
"""
from compressor import __version__ as VERSION
from enum import Enum

ENC = "utf-8"
BYTE = 8
BUFF_SIZE = 1024
LEFT = b"0"
RIGHT = b"1"


class Actions:
    """Possible operations the tool can do."""
    COMPRESS = 0
    EXTRACT = 1

    @classmethod
    def from_flags(cls, compress: bool, extract: bool):
        if compress:
            return cls.COMPRESS
        if extract:
            return cls.EXTRACT
