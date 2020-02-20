.. _bridges:vhpidirect:

VHPIDIRECT
##########

This is a bridge between VUnit's external VHDL API and C, through GHDL's VHPIDIRECT
features (see :ref:`ghdl:USING:Foreign`). A Python class (named ``VHPIDIRECT``) provides
helper functions to (re)use a C API (``vhpidirect_user.h``, ``grt.ver`` and/or
``stubs.c``) with VUnit's ``add_builtins`` and ``set_sim_option("ghdl.elab_flags", ...)``.
Examples of how to use this bridge are shown in :ref:`examples:vhpidirect`.

.. NOTE:: In the latest stable release of GHDL (v0.36), mcode backend does not support
  VHPIDIRECT. Moreover, using LLVM or GCC backends is suggested, as these generate
  executable files and are supported in a wider range of platforms.

.. NOTE:: For GHDL to generate PIE executable files, it needs to be configured with option
  ``--default-pic``. Moreover, loading ELF binaries dynamically is a *hackish* procedure
  that takes advantage of PIE ELF binaries and shared libraries having a common structure
  on GNU/Linux. However, this does not work on Windows (see `ghdl/ghdl#803 <https://github.com/ghdl/ghdl/issues/803>`_).
  As a result:

  * GHDL needs to be enhanced to allow building designs as shared libraries instead of
    executable binaries (see `ghdl/ghdl#800 <https://github.com/ghdl/ghdl/issues/800>`_).
  * or, build features in VUnit need to be extended to use ``ghdl --bind``,
    ``ghdl --list-link`` and gcc/clang in order to generate a ``*.dll`` on Windows.
  * or, a helper method need to be added to this class to use gcc/clang.

Implementation details
======================

``vhpidirect_user.h`` is the C implementation of the interface. It uses an array of
pointers (``uint8_t *D[256];``) to keep a reference to all the buffers that are shared
between C and VHDL.

.. NOTE:: Users that need to share more than 256 pointers, can and should include their
  own copy of this header file. Actually, in example :ref:`examples:copy` the provided
  header file is not used. Instead, functions are implemented in ``main.c``.

``stubs.c`` is to be used when multiple tests are handled in a single ``run.py`` file
(i.e. by the same VUnit object), but some of them do NOT use external modes. Since
builtins are compiled once only, every test (binary) needs to have placeholders for the C
functions that VHDL expects to use. ``stubs.c`` provides *dummy* definitions of the C API.
Note that these will produce errors if executed at runtime.

``grt.ver`` is to be used when the ELF file built with GHDL is to be loaded dynamically.
By default, GHDL hides most of the global symbols. Providing this file as an elaboration
option ensures that the functions of the C API are visible. Script ``corun.py`` in example
:ref:`examples:buffer` shows how to dynamically load and execute the simulation from Python.

extfnc mode
-----------

As explained in :ref:`vunit:data_types_library:external`, mode *extfnc* is expected to be
used when data is not available in the same memory space as the VHDL simulation. For
example, when libraries such as `gRPC <https://grpc.io/>`_, `ZeroMQ <https://zeromq.org/>`_
or `netpp <https://section5.ch/index.php/netpp/>`_ are used to co-execute simulations in
remote targets. Hence, ``write_*/read_*`` function bodies provided in ``vhpidirect_user.h``
are for testing purposes. In practice, developers willing to use this mode are expected
to provide their own custom header file.

Note that this is the difference between *extfnc* and *extacc*: with *extacc*, there is
no explicit callback when VHDL modifies a value in a shared buffer. Conversely, with
*extfnc*, VHDL cannot modify a value without a callback.

Python interface
================

.. autoclass:: cosim.vhpidirect.VHPIDIRECT()
