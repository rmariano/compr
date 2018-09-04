"""Utilities and functions used throughout the application"""
import os
import struct
import sys
from functools import singledispatch, wraps
from typing import Callable, Union, overload

from compressor.constants import ENC


def default_filename(filename: str, suffix: str = "comp") -> str:
    """Default composition for the name to be used.
    If suffix is not specified, use ``comp`` as default one, assuming the
    operation in course is a compression.
    """
    basename = os.path.basename(filename)
    return "{basename}.{suffix}".format(basename=basename, suffix=suffix)


def endianess_prefix(parm_type=str) -> Union[str, bytes]:
    """
    Return the prefix to be used in struct.{pack,unpack} according
    to the system architecture (little/big endian, 32/64 bits).

    :param parm_type: str | bytes depending on the version
    :return:          '<' for little endian
                      '>' big endian
    """
    value = "<" if sys.byteorder == "little" else ">"
    if parm_type is bytes:
        return bytes(value, encoding=ENC)
    return value


def patched_struct(struct_function: Callable) -> Callable:
    """
    Prefix the endian code according to the architecture by patching the
    library.

    This decorator patches the function from the struct module, based on
    the architecture of the running system.

    :param struct_function: struct.pack | struct.unpack
    :return:                decorated <struct_function>
    """

    @wraps(struct_function)
    def wrapped(code: Union[str, bytes], *args):
        """
        Decorated version of the struct original function

        :param args: The *args of the original function
        """
        endian = endianess_prefix(type(code))
        assert type(code) is type(endian), "Type mismatch: {} and {}".format(
            type(code), type(endian)
        )
        if not code.startswith(endian):  # type: ignore
            code = endian + code  # type: ignore
        return struct_function(code, *args)

    return wrapped


@patched_struct
def pack(code, *args):
    """Original struct.pack with the decorator applied.
    Will change the code according to the system's architecture.
    """
    return struct.pack(code, *args)


@patched_struct
def unpack(code, *args):
    """Original struct.unpack with the decorator applied.
    Will change the code according to the system's architecture.
    """
    return struct.unpack(code, *args)


@singledispatch
def tobinary(obj) -> str:
    """Convert <obj> to the binary representation"""
    return str(obj)


@overload  # type: ignore
@tobinary.register(int)
def _(number) -> str:
    """Return the ``str`` for the binary representation of ``number``.
    Examples::

        >>> tobinary(42)
        '101010'
    """
    return format(number, "b")


@overload
@tobinary.register(str)
@tobinary.register(bytes)
def _(str_hex):  # type: ignore
    """If it is a string, we assume it's the HEX representation of the number.

    For example::

        >>> tobinary('ff')  # 255
        '11111111'

        >>> tobinary(b'a')  # 10
        '1010'
    """
    return tobinary(int(str_hex, 16))


class StreamFile:
    """Read a file by chunks, streaming each one at the time

    Use as a context manager and iterable object.

    >>> with StreamFile("some file", 1000) as source:
    ...     for buffer in source:
    ...         do_something_with(buffer)
    """

    def __init__(self, filename: str, chunk_size: int) -> None:
        self.filename = filename
        self.chunk_size = chunk_size
        self._data_source = None

    def __enter__(self):
        self._data_source = open(self.filename)
        return self

    def __exit__(self, ex_type, ex_value, ex_tb):
        self._data_source.close()

    def __iter__(self):
        return self

    def __next__(self):
        data = self._data_source.read(self.chunk_size)
        if not data:
            raise StopIteration
        return data
