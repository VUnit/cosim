.. _bridges:

Bridges
#######

Bridges contain VHDL packages, matching C headers and/or Python classes. Each bridge provides the glue logic between a VHDL API and some other API in VHDL and/or C (bindings).

.. NOTE:: `GHDL <https://github.com/ghdl/ghdl>`_, the only free and open source simulator for VHDL supported by VUnit, features VPI and a limited subset of VHPI named VHPIDIRECT. Since co-simulation of VHDL and Python through VPI is already supported and documented by `cocotb <https://github.com/cocotb/cocotb>`_, this project is mostly focused on VHPIDIRECT.

Available modules:

:ref:`bridges:vhpidirect`
    C bindings for VUnit's external VHDL API (see :ref:`vunit:data_types_library`).

.. toctree::
   :maxdepth: 2
   :hidden:

   vhpidirect
