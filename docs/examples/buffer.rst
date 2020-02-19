.. _examples:buffer:

Buffer
######

This example shows how to use :class:`cosim.vhpidirect.VHPIDIRECT` (see :ref:`bridges:vhpidirect` to interact with VUnit's internal ``string_ptr``/``byte_vector_ptr`` and/or ``integer_vector_ptr``, from C and/or Python.

* ``run.py``: supports a custom CLI option, ``--build``, that will set ``VU.set_sim_option("ghdl.elab_e", True)``.

   * :func:`cosim.vhpidirect.VHPIDIRECT.bridge` is used to enable external mode support for ``string_ptr`` and `integer_vector_ptr` (see :ref:`vunit:data_types_library`).
   * :func:`cosim.vhpidirect.VHPIDIRECT.include` is used to build C sources with the provided C API/headers.
   * :func:`cosim.vhpidirect.VHPIDIRECT.verscript` is used to provide a version script that matches the functions in the C API.
   * The ``post_func`` provided by :ref:`bridges:vhpidirect` (see :func:`cosim.vhpidirect.VHPIDIRECT.post_func`) is used to save in subdir `vunit_out/cosim` the CLI args that correspond to each testbench.

* ``corun.py``: allows to dynamically load and run any of the simulation binaries built with ``run.py``. Given a testbench name, it finds the corresponding binary and arguments JSON file. Then, it is loaded dynamically and data buffers allocated in Python are shared with the simulation.

Example session:

.. CODE:: bash

    # python3 run.py --build -v
    ...

    # ls vunit_out/cosim/
    tb_external_byte_vector.json  tb_external_integer_vector.json  tb_external_string.json

    # python3 corun.py tb_external_byte_vector
    ...

.. NOTE:: GHDL with mcode backend does NOT generate executable binaries. In order to use the two-step workflow, eithe LLVM or GCC backends need to be used.

.. NOTE:: ``corun.py`` depends on :mod:`cosim.utils`, which requires some additional dependencies. File ``requirements.txt`` can be used to install all of them at once.
