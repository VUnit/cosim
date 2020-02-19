"""
C/Python co-simulation utilities
"""

# pylint:disable=wrong-import-order

import sys
from sys import platform
from pathlib import Path
from base64 import b64encode
from io import BytesIO
import ctypes
import _ctypes  # type: ignore
import numpy  # type: ignore
from PIL import Image  # type: ignore


def dlopen(path):
    """
    Open/load a PIE binary or a shared library.
    """
    if not Path(path).is_file():
        print("Executable binary not found: " + path)
        sys.exit(1)
    try:
        return ctypes.CDLL(path)
    except OSError:
        print(
            "Loading executables dynamically seems not to be supported on this platform"
        )
        sys.exit(1)


def dlclose(obj):
    """
    Close/unload a PIE binary or a shared library.

    :param obj: object returned by ctypes.CDLL when the resource was loaded
    """
    if platform == "win32":
        _ctypes.FreeLibrary(obj._handle)  # pylint:disable=protected-access,no-member
    else:
        _ctypes.dlclose(obj._handle)  # pylint:disable=protected-access,no-member


def enc_args(args):
    """
    Convert args to a suitable format for a foreign C function.

    :param args: list of strings
    """
    xargs = (ctypes.POINTER(ctypes.c_char) * len(args))()
    for idx, arg in enumerate(args):
        xargs[idx] = ctypes.create_string_buffer(arg.encode("utf-8"))
    return xargs


def byte_buf(lst):
    """
    Convert array to a string buffer (uint8_t* in C).

    :param lst: list of naturals range [0,255]
    """
    return ctypes.create_string_buffer(bytes(lst), len(lst))


def int_buf(lst, bpw=4, signed=True):
    """
    Convert array to a string buffer (uint8_t* in C).

    :param lst: list of integers
    :param bpw: number of bytes per word/integer
    :param signed: whether to encode the numbers as signed
    """
    out = [None] * 4 * len(lst)
    for idx, val in enumerate(lst):
        out[idx * 4 : idx * 4 + 4] = (val).to_bytes(
            bpw, byteorder="little", signed=signed
        )
    return byte_buf(out)


def read_byte_buf(buf):
    """
    Read byte/string buffer (uint8_t* in C) as a list of numbers.
    """
    return read_int_buf(buf, bpw=1, signed=False)


def read_int_buf(buf, bpw=4, signed=True):
    """
    Read byte/string buffer as a list of numbers.

    :param buf: byte/string buffer (uint8_t* in C) to read from
    :param bpw: number of bytes per word/integer
    :param signed: whether to decode the numbers as signed
    """
    out = [None] * int(len(buf) / bpw)
    if bpw == 1:
        for idx, val in enumerate(buf):
            out[idx] = int.from_bytes(val, byteorder="little", signed=signed)
    else:
        for idx, _ in enumerate(out):
            out[idx] = int.from_bytes(
                buf[idx * bpw : idx * bpw + bpw], byteorder="little", signed=signed
            )
    return out


def b64enc_int_list(lst, width, height):
    """
    Encode list of numbers as a base64 encoded PNG image.

    :param lst: list of pixel values (len = height x width) in row-major order
    :param width: spatial width
    :param height: spatial height
    """
    buf = BytesIO()
    Image.fromarray(
        numpy.array(numpy.reshape(lst, (height, width)), dtype=numpy.uint16)
    ).save(buf, format="PNG")
    return b64encode(buf.getvalue()).decode("utf8")


def b64enc_list_of_int_lists(lst, width, height):
    """
    Convert list of lists of numbers to list of base64 encoded PNG images.

    :param lst: list of lists of pixel values (len = height x width) in row-major order
    :param width: spatial width
    :param height: spatial height
    """
    b64 = [[] for idx in range(len(lst))]
    for idx, val in enumerate(lst):
        b64[idx] = b64enc_int_list(val, width, height)
    return b64
