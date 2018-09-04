"""
``compressor.core``

Low-level functionality with the core of the process that the main
program makes use of.

It contains auxiliary functions.
"""
import binascii
import heapq
from collections import Counter
from functools import total_ordering
from typing import List, Sequence, io  # type: ignore

from compressor.constants import BUFF_SIZE, BYTE, ENC, LEFT, RIGHT
from compressor.util import (StreamFile, default_filename, pack, tobinary,
                             unpack)


@total_ordering
class CharNode:
    """
    Object that wraps/encapsulates the definition of a character
    in the text being processed.
    Used for comparison, and helper with its properties & methods.
    """

    def __init__(self, value, freq, left=None, right=None) -> None:
        """
        Represent a character as a node in a tree.

        :param value: the original character
        :param freq:  float with the occurrence average of `value`
                      in the processed text.
        :param left:  left child of this node.
        :param right: right child of this node in the tree.
        """
        self._value = value
        self.freq = freq
        self.left = left
        self.right = right

    def __le__(self, other) -> bool:
        """
        Compare if this character is less or equal than another
        one of the same kind.

        :param other: Another CharNode with properties.
        :return:      self <= other
        :rtype: bool
        """
        if self.__class__ is other.__class__:
            return self.freq <= other.freq
        return NotImplemented

    def __eq__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.freq == other.freq
        return NotImplemented

    def __hash__(self):
        return hash(self.freq)

    @property
    def value(self):
        """Expose the value being hold as read-only."""
        return self._value

    @property
    def leaf(self) -> bool:
        """
        Checks if the current node is a leaf in the tree. It is a leaf when it
        does not have any children (neither left nor right).

        :return: True if this node has no children, False otherwise.
        """
        return self.left is None and self.right is None


def create_tree_code(charset: List[CharNode]) -> CharNode:
    """
    Receives a :list: of :CharNode: (characters) charset,
    namely leaves in the tree, and returns a tree with the corresponding
    prefix-free code.

    :param charset: iterable with all the characters to process.

    :return:        iterable with a tree of the prefix-free code
                    for the charset.
    """
    alpha_heap = charset
    heapq.heapify(alpha_heap)

    for _ in charset[:-1]:
        left_char = heapq.heappop(alpha_heap)
        right_char = heapq.heappop(alpha_heap)

        new_symbol = CharNode(
            value='{0.value}{1.value}'.format(left_char, right_char),
            freq=left_char.freq + right_char.freq,
            left=left_char,
            right=right_char
        )
        heapq.heappush(alpha_heap, new_symbol)
    return heapq.heappop(alpha_heap)


def parse_tree_code(tree: CharNode, table: dict = None,
                    code: bytes = b'') -> dict:
    """
    Given the tree with the chars-frequency processed, return a table that
    maps each character with its binary representation on the new code:

        left --> 0

        right --> 1

    :param tree:  iterable with the tree as returned by `create_tree_code`
    :param table: Map with the translation for the characters to its code in
                  the new system (prefix-free).
    :param code:  The code prefix so far.

    :return:      Mapping with with the original char to its new code.
    """
    table = table or {}
    if tree.leaf:
        table[tree.value] = code
        return table
    table.update(parse_tree_code(tree.left, table, code + LEFT))
    table.update(parse_tree_code(tree.right, table, code + RIGHT))
    return table


def process_frequencies(stream: Sequence[str]) -> List[CharNode]:
    """
    Given a stream of text, return a list of CharNode with the frequencies
    for each character.

    :param stream: sequence with all the characters.
    """
    counts = Counter(stream)
    return [CharNode(value=value, freq=freq) for value, freq in counts.items()]


def save_table(dest_file: io, table: dict) -> None:
    """
    Store the table in the destination file.
        c: char
        L: code of c (unsigned Long)

    :param dest_file: opened file where to write the `table`.
    :param table:     Mapping table with the chars and their codes.
    """
    offset = len(table)
    tokens = [(char.encode(ENC), int(b'1' + codec, base=2))
              for char, codec in table.items()]

    chars, codecs = zip(*tokens)

    dest_file.write(pack('i', offset))
    dest_file.write(pack('{0}c'.format(offset), *chars))
    dest_file.write(pack('{0}L'.format(offset), *codecs))


def process_line_compression(buffer_line: str, output_file: io,
                             table: dict) -> None:
    """
    Transform `buffer_line` into the new code, per-byte, based on `table`
    and save the new byte-stream into `output_file`.

    :param buffer_line: a chunk of the text to process.
    :param output_file: The opened file where to write the result.
    :param table:       Translation table for the characters in `buffer_line`.
    """
    bitarray = []  # type: list
    chr_buffer = b''
    for char in buffer_line:
        encoded_char = table[char]
        chr_buffer += encoded_char
        bitarray.extend(int(chr(x)) for x in encoded_char)

    array_str = ''.join(str(x) for x in bitarray)
    # Add a sentinel first bit
    array_str = '1' + array_str
    array_str += '0' * (BYTE - (len(array_str) % BYTE))  # 0-pad

    stream = hex(int(array_str, 2))[2:]
    block = binascii.a2b_hex(stream)
    block_length = len(array_str) // BYTE
    original_length = len(buffer_line)

    output_file.write(pack('I', block_length))
    output_file.write(pack('I', original_length))
    output_file.write(block)


def compress_and_save_content(input_filename: str,
                              output_file: io, table: dict) -> None:
    """
    Opens and processes <input_filename>. Iterates over the file and writes
    the contents on output_file.

    :param input_filename: the source to be compressed
    :param output_file:    opened file where to write the outcome
    :param table:          mapping table for the char encoding
    """
    with StreamFile(input_filename, BUFF_SIZE) as source:
        for buff in source:
            process_line_compression(buff, output_file, table)


def _sizeof(code: str) -> int:
    sizes = {'i': 4, 'c': 1, 'L': 4, 'I': 4}
    return sizes.get(code, 1)


def retrieve_table(dest_file: io) -> dict:
    """
    Read the binary file, and return the translation table as a reversed
    dictionary.
    """
    offset, *_ = unpack('i', dest_file.read(_sizeof('i')))
    chars = dest_file.read(offset * _sizeof('c'))
    codes = dest_file.read(offset * _sizeof('L'))

    chars = unpack('{}c'.format(offset), chars)
    codes = unpack('{}L'.format(offset), codes)
    return {"b{0}".format(tobinary(code)): str(char, encoding=ENC)
            for char, code in zip(chars, codes)}


def _save_checksum(ofile: io, checksum: int):
    """Persist the number of bytes as the first byte in <ofile>."""
    ofile.write(pack('L', checksum))


def _retrieve_checksum(ifile: io) -> int:
    rawdata = ifile.read(_sizeof('L'))
    return unpack('L', rawdata)[0]


def save_compressed_file(filename: str, table: dict, checksum: int,
                         dest_file: str = '') -> None:
    """
    Given the original file by its `filename`, save a new one.
    `table` contains the new codes for each character on `filename`.
    """
    new_file = dest_file or default_filename(filename)

    with open(new_file, 'wb') as target:
        _save_checksum(target, checksum)
        save_table(target, table)
        compress_and_save_content(filename, target, table)


def _decode_block(binary_content: bytes, table: dict,
                  block_length: int) -> str:
    """Transform the compressed content of a block into the original text."""
    newchars = []
    cont = binascii.hexlify(binary_content)
    bitarray = tobinary(cont)
    # Ignore first bit, sentinel
    bitarray = bitarray[1:]
    window_start, window_end = 0, 1
    part = bitarray[window_start:window_end]
    restored = 0  # bytes
    while part:
        char = table.get(bitarray[window_start:window_end], False)
        while not char and bitarray[window_start:window_end]:
            window_end += 1
            char = table.get(bitarray[window_start:window_end], False)
        newchars.append(char)
        restored += 1
        if restored == block_length:
            break
        window_start, window_end = window_end, window_end + 1
        part = bitarray[window_start:window_end]
    return ''.join(newchars)[:block_length]


def decode_file_content(compfile: io, table: dict, checksum: int) -> str:
    """
    Reconstruct the remaining part of the <compfile>, starting right after
    the metadata, decoding each bit according to the <table>.
    """
    original_stream = ''
    next_block = compfile.read(_sizeof('I'))
    while len(original_stream) < checksum and next_block:
        block_size, *_ = unpack('I', next_block)
        block_length, *_ = unpack('I', compfile.read(_sizeof('I')))
        binary_content = compfile.read(block_size)
        retrieved = _decode_block(binary_content, table, block_length)

        original_stream += retrieved
        next_block = compfile.read(_sizeof('I'))
    return original_stream


def _reorganize_table_keys(table: dict) -> dict:
    """Change the keys of the table to be more easily readable: bytes->str"""
    return {k[2:]: v for k, v in table.items()}


def retrieve_compressed_file(filename: str, dest_file: str = '') -> None:
    """
    EXTRACT - Reconstruct the original file from the compressed copy.
    Write the output in the indicated `dest_file`.
    """
    with open(filename, 'rb') as src:
        checksum = _retrieve_checksum(src)
        map_table = retrieve_table(src)
        table = _reorganize_table_keys(map_table)

        dest_filename = dest_file or default_filename(filename, suffix='extr')
        stream = decode_file_content(src, table, checksum)
        # Dump the decoded extraction into its destination
        with open(dest_filename, 'w+') as out:
            out.write(stream)
