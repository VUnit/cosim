"""
Copy
----

Copy from a vector with mode extacc to another vector with mode extfnc
"""

from pathlib import Path
from subprocess import check_call
from vunit import VUnit
from cosim.vhpidirect import VHPIDIRECT

SRC = Path(__file__).parent / "src"

C_OBJ = SRC / "cp.o"
# Compile C application to an object
check_call(["gcc", "-fPIC", "-c", str(SRC / "cp.c"), "-o", C_OBJ])

# Enable the external feature for strings
VU = VUnit.from_argv(vhdl_standard="2008", compile_builtins=False)
VU.add_builtins(VHPIDIRECT().bridge({"string": True}))

VU.add_library("lib").add_source_files(SRC / "tb_extcp_*.vhd")

# Add the C object to the elaboration of GHDL
VU.set_sim_option("ghdl.elab_flags", ["-Wl," + str(C_OBJ)])

VU.main()
