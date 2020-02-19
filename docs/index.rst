.. centered:: |shieldVunit|_ |shieldCosim|_ |shieldGitter|_ |shieldTwitter|_

.. |shieldVunit| image:: https://img.shields.io/badge/VUnit/vunit-0c479d.svg?longCache=true&style=flat-square&logo=github
.. _shieldVunit: https://github.com/VUnit/vunit

.. |shieldCosim| image:: https://img.shields.io/badge/VUnit/cosim-000000.svg?longCache=true&style=flat-square&logo=github&logoColor=fdbe00
.. _shieldCosim: https://github.com/VUnit/cosim

.. |shieldGitter| image:: https://img.shields.io/gitter/room/VUnit/vunit.svg?longCache=true&style=flat-square&logo=gitter&logoColor=4db797&color=4db797
.. _shieldGitter: https://gitter.im/VUnit/vunit

.. |shieldTwitter| image:: https://img.shields.io/twitter/follow/VUnitFramework.svg?longCache=true&style=flat-square&color=1DA1F2&label=%40VUnitFramework&logo=twitter&logoColor=fff
.. _shieldTwitter: https://www.twitter.com/VUnitFramework

VUnit cosim
===========

**VUnit** is an open source unit testing framework for VHDL/SystemVerilog, which features the
functionality needed to realise continuous and automated testing of HDL code.
VUnit doesn't replace but rather complements traditional testing methodologies by
supporting a *"test early and often"* approach through automation. :ref:`Read more <vunit:about>`

**VUnit cosim** follows the same philosophy to support co-simulation (co-execution) of VHDL along with
software applications written in a different language (typically C/C++ or Python). The content of this module is organised in bridges, examples and utils:

* :ref:`bridges`: glue logic between a :ref:`external VHDL API <vunit:data_types_library>` (or another bridge) and some other API in VHDL and/or C (bindings).

* :ref:`examples`: working demo projects that use some utils and/or bridges.

* :ref:`utils`: helper functions in Python (based on ctypes, base64, numpy and Pillow) which are useful for interacting with C-alike executables.

.. toctree::
   :maxdepth: 3
   :hidden:

   bridges/index
   examples/index
   utils
   genindex
   py-modindex
