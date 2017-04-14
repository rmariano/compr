"""Utilities and functions used throughout the application"""
import struct
import sys
from functools import wraps
from typing import Callable, Union

from compressor.constants import ENC


def brand_filename(filename: str) -> str:
    """Default composition for the name to be used"""
    return "{0}.comp".format(filename)


def endianess_prefix(parm_type=str) -> Union[str, bytes]:
    """
    Return the prefix to be used in struct.{pack,unpack} according
    to the system architecture (little/big endian, 32/64 bits).

    :param parm_type: str | bytes depending on the version
    :return:          '<' for little endian
                      '>' big endian
    """
    value = '<' if sys.byteorder == 'little' else '>'
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
            type(code), type(endian))
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
