"""
Buffer
------

An array of type ``uint8_t`` is allocated in a C application and some values
are written to the first ``1/3`` positions. Then, the VHDL simulation is
executed, where the (external) array/buffer is used.

In the VHDL testbenches, two vector pointers are created, each of them using
a different access mechanism (``extfunc`` or ``extacc``). One of them is used to copy
the first ``1/3`` elements to positions ``[1/3, 2/3)``, while incrementing each value
by one. The second one is used to copy elements from ``[1/3, 2/3)`` to ``[2/3, 3/3)``,
while incrementing each value by two.

When the simulation is finished, the C application checks whether data was successfully
copied/modified. The content of the buffer is printed both before and after the
simulation.
"""

from sys import argv
from pathlib import Path
from subprocess import check_call
from vunit import VUnit
from cosim.vhpidirect import VHPIDIRECT

COSIM = VHPIDIRECT()

SRC = Path(__file__).parent / "src"

BUILD_ONLY = False
if "--build" in argv:
    argv.remove("--build")
    BUILD_ONLY = True

# Compile C applications to objects
C_IOBJ = SRC / "imain.o"
C_BOBJ = SRC / "bmain.o"

for val in [["int32_t", C_IOBJ], ["uint8_t", C_BOBJ]]:
    check_call(
        ["gcc", "-fPIC", "-DTYPE=%s" % val[0]]
        + ["-I%s" % inc for inc in COSIM.include]
        + ["-c", str(SRC / "main.c"), "-o", val[1]]
    )

# Enable the external feature for strings/byte_vectors and integer_vectors
VU = VUnit.from_argv(vhdl_standard="2008", compile_builtins=False)
VU.add_builtins(COSIM.bridge({"string": True, "integer_vector": True}))

LIB = VU.add_library("lib")
LIB.add_source_files(SRC / "tb_ext_*.vhd")

# Add the C object to the elaboration of GHDL
for tb in LIB.get_test_benches(pattern="*tb_ext*", allow_empty=False):
    tb.set_sim_option("ghdl.elab_flags", ["-Wl," + str(C_BOBJ)])
for tb in LIB.get_test_benches(pattern="*tb_ext*_integer*", allow_empty=False):
    tb.set_sim_option("ghdl.elab_flags", ["-Wl," + str(C_IOBJ)], overwrite=True)

if BUILD_ONLY:
    VU.set_sim_option("ghdl.elab_flags", [COSIM.verscript()], overwrite=False)
    VU.set_sim_option("ghdl.elab_e", True)
    VU._args.elaborate = True  # pylint: disable=protected-access
    VU.main(post_run=COSIM.post_func)
else:
    VU.main()
