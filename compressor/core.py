import heapq
import struct
import binascii
import sys
from collections import Counter


ENC = 'utf-8'
BYTE = 8
BUFF_SIZE = 1024


def endianess_prefix(parm_type=str):
    value = '<' if sys.byteorder == 'little' else '>'
    if parm_type is bytes:
        return bytes(value, encoding=ENC)
    return value


def patched_struct(f):
    """Prefix the endian code according to the architecture by patching the
    library."""
    def wrapped(*args):
        code = args[0]
        endian = endianess_prefix(type(code))
        assert type(code) is type(endian), "Type mismatch: {} and {}".format(type(code), type(endian))
        if not code.startswith(endian):
            # Note: it is NOT possible to use `.format` here, must be `+`
            # values can be bytes or str
            code = endian + code
        return f(code, *args[1:])
    return wrapped


struct.pack = patched_struct(struct.pack)
struct.unpack = patched_struct(struct.unpack)


class CharNode(object):

    def __init__(self, value, freq, left=None, right=None):
        self.value = value
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

    def __le__(self, other):
        return self.freq <= other.freq

    def __gt__(self, other):
        return self.freq > other.freq

    def __ge__(self, other):
        return self.freq >= other.freq

    def __eq__(self, other):
        return self.freq == other.freq

    def __ne__(self, other):
        return self.freq != other.freq

    @property
    def leaf(self):
        return self.left is None and self.right is None


def create_tree_code(C):
    """Receives a :list: of :CharNode: (characters) C,
    namely leaves in the tree, and returns a tree with the corresponding
    prefix-free code."""
    n = len(C)
    Q = C
    heapq.heapify(Q)
    for _ in range(1, n):
        z = CharNode('', 0)
        z.left = x = heapq.heappop(Q)
        z.right = y = heapq.heappop(Q)
        z.freq = x.freq + y.freq
        heapq.heappush(Q, z)
    return heapq.heappop(Q)


def parse_tree_code(tree, table=None, code=b''):
    """Given the tree with the chars-frequency processed, return a table that
    maps each character with its binary representation on the new code:
    left --> 0
    right --> 1
    """
    table = table or {}
    LEFT = b'0'
    RIGHT = b'1'
    if tree.leaf:
        table[tree.value] = code
        return table
    table.update(parse_tree_code(tree.left, table, code+LEFT))
    table.update(parse_tree_code(tree.right, table, code+RIGHT))
    return table


def process_frequencies(stream):
    """Given a stream of text, return a list of CharNode with the frequencies
    for each character."""
    counts = Counter(stream)
    return [CharNode(value=value, freq=freq) for value, freq in counts.items()]


def save_table(dest_file, table):
    """Store the table in the destination file.
    c: char
    L: code of c (unsigned Long)"""
    offset = len(table)
    tokens = [(bytes(char, encoding=ENC), b'1' + v) for char, v in table.items()]
    content = struct.pack('i', offset)
    content += struct.pack('{}c'.format(offset), *[t[0] for t in tokens])
    content += struct.pack('{}L'.format(offset), *[int(t[1], base=2) for t in tokens])
    dest_file.write(content)


def process_line_compression(buffer_line, output_file, table):
    """Transform :buffer_line: into the new code, per-byte, based on :table:
    and save the new byte-stream into :output_file:."""
    bitarray = []
    buff = []
    chr_buffer = b''
    for char in buffer_line:
        encoded_char = table[char]
        chr_buffer += encoded_char
        bitarray.extend(int(chr(x)) for x in encoded_char)
    bitarray = ''.join(map(str, bitarray))
    # Add a sentinel first bit
    bitarray = '1' + bitarray
    bitarray += '0' * (BYTE - (len(bitarray) % BYTE))  # 0-pad

    stream = hex(int(bitarray, 2))[2:]
    block = binascii.a2b_hex(stream)
    block_length = len(bitarray) // BYTE
    original_length = len(buffer_line)

    output_file.write(struct.pack('I', block_length))
    output_file.write(struct.pack('I', original_length))
    output_file.write(block)


def compress_and_save_content(input_filename, output_file, table):
    """Opens and processes <input_filename>. Iterates over the file and writes
    the contents on output_file."""
    with open(input_filename, 'r') as f:
        buff = f.read(BUFF_SIZE)
        while buff:
            process_line_compression(buff, output_file, table)
            buff = f.read(BUFF_SIZE)
    return


def _sizeof(code):
    sizes = {'i': 4, 'c': 1, 'L': 4, 'I': 4}
    return sizes.get(code, 1)


def retrieve_table(dest_file):
    """Read the binary file, and return the translation table as a reversed
    dict."""
    offset, *_ = struct.unpack('i', dest_file.read(_sizeof('i')))
    chars = dest_file.read(offset * _sizeof('c'))
    codes = dest_file.read(offset * _sizeof('L'))
    chars = struct.unpack('{}c'.format(offset), chars)
    codes = struct.unpack('{}L'.format(offset), codes)
    return {bin(code)[1:]: str(char, encoding=ENC) for char, code in zip(chars, codes)}


def _brand_filename(filename):
    return "{}.comp".format(filename)


def _save_checksum(ofile, checksum):
    """Persist the number of bytes as the first byte in <ofile>."""
    ofile.write(struct.pack('L', checksum))
    return


def _retrieve_checksum(ifile):
    rawdata = ifile.read(_sizeof('L'))
    return struct.unpack('L', rawdata)[0]


def save_compressed_file(filename, table, checksum, dest_file=None):
    """Given the original file by its <filename>, save a new one.
    <table> contains the new codes for each character on <filename>"""
    new_file = dest_file if dest_file else _brand_filename(filename)
    with open(new_file, 'wb') as f:
        _save_checksum(f, checksum)
        save_table(f, table)
        compress_and_save_content(filename, f, table)
    return


def _decode_block(binary_content, table, block_length):
    """Transform the compressed content of a block into the original text."""
    newchars = []
    cont = binascii.hexlify(binary_content)
    bitarray = bin(int(cont, 16))[2:]
    # Ignore first bit, sentinel
    bitarray = bitarray[1:]
    i, j = 0, 1
    part = bitarray[i:j]
    restored = 0  # bytes
    while part:
        char = table.get(bitarray[i:j], False)
        while not char and bitarray[i:j]:
            j += 1
            char = table.get(bitarray[i:j], False)
        newchars.append(char)
        restored += 1
        if restored == block_length:
            break
        i, j = j, j + 1
        part = bitarray[i:j]
    return ''.join(newchars)[:block_length]


def decode_file_content(compfile, table, checksum):
    """Reconstruct the remaining part of the <compfile>, starting right after
    the metadata, decoding each bit according to the <table>."""
    original_stream = ''
    next_block = compfile.read(_sizeof('I'))
    while len(original_stream) < checksum and next_block:
        block_size, *_ = struct.unpack('I', next_block)
        block_length, *_ = struct.unpack('I', compfile.read(_sizeof('I')))
        binary_content = compfile.read(block_size)
        retrieved = _decode_block(binary_content, table, block_length)

        if len(original_stream + retrieved) > checksum:
            break
        original_stream += retrieved
        next_block = compfile.read(_sizeof('I'))
    return original_stream


def _reorganize_table_keys(table):
    """Change the keys of the table to be more easily readable: bytes->str"""
    return {k[2:]: v for k, v in table.items()}


def retrieve_compressed_file(filename, dest_file=None):
    """EXTRACT - Reconstruct the original file from the compressed copy.
    Write the output in the indicated <dest_file>"""
    with open(filename, 'rb') as f:
        checksum = _retrieve_checksum(f)
        t = retrieve_table(f)
        table = _reorganize_table_keys(t)
        dest_filename = dest_file if dest_file else "{}.extr".format(filename)
        stream = decode_file_content(f, table, checksum)
        # Dump the decoded extraction into its destination
        with open(dest_filename, 'w+') as out:
            out.write(stream)
