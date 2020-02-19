"""
Buffer: dynamically loading a simulation from Python
----------------------------------------------------

Given a PIE executable and a set of CLI args in a JSON file, execute a simulation twice:

* First, load it dynamically and execute the simulation without shared data buffers.
* Then, load it again, allocate data buffers from Python, execute the simulation,
and check the modified buffers from Python.
"""

import argparse
import sys
from pathlib import Path
from json import load
from cosim.utils import (
    enc_args,
    dlopen,
    dlclose,
    byte_buf,
    int_buf,
    read_byte_buf,
    read_int_buf,
)

PARSER = argparse.ArgumentParser()
PARSER.add_argument(
    "testbench", type=str, nargs="+", help="name of a pre-built testbench"
)
PARSER.add_argument(
    "--output-path",
    type=str,
    dest="output_path",
    default=str(Path(__file__).parent / "vunit_out"),
    help="output path (default: 'vunit_out')",
)

PARGS = PARSER.parse_args()

with (
    Path(PARGS.output_path) / "cosim" / ("%s.json" % PARGS.testbench[0])
).open() as json_file:
    ARGS = load(json_file)
    if "integer" not in PARGS.testbench[0]:
        NEW_BUF = byte_buf
        READ_BUF = read_byte_buf
    else:
        NEW_BUF = int_buf
        READ_BUF = read_int_buf

XARGS = enc_args([ARGS["bin"]] + ARGS["sim"])

print("\nREGULAR EXECUTION")
GHDL = dlopen(ARGS["bin"])
try:
    GHDL.main(len(XARGS) - 1, XARGS)
# TOFIX With VHDL 93, the execution is Aborted and Python exits here
except SystemExit as exc:
    if exc.code != 0:
        sys.exit(exc.code)
dlclose(GHDL)

print("\nPYTHON ALLOCATION")
GHDL = dlopen(ARGS["bin"])

DATA = [111, 122, 133, 144, 155]

# Two pointers/buffers are to be allocated
BUF = [[] for c in range(2)]

# Allocate and initialize shared data buffer
BUF[1] = NEW_BUF(DATA + [0 for x in range(2 * len(DATA))])

# Fill 'params' vector
BUF[0] = int_buf(
    [-(2 ** 31) + 10, -(2 ** 31), 3, 0, len(DATA)]  # clk_step  # update  # block_length
)

for x, v in enumerate(BUF):
    GHDL.set_string_ptr(x, v)

for i, v in enumerate(READ_BUF(BUF[1])):
    print("py " + str(i) + ": " + str(v))

GHDL.ghdl_main(len(XARGS) - 1, XARGS)

for i, v in enumerate(READ_BUF(BUF[1])):
    print("py " + str(i) + ": " + str(v))

dlclose(GHDL)
