.. _examples:

Examples
########

.. NOTE:: Since this project is not distributed through PyPI yet, and because it depends
   on a specific branch of VUnit, it is suggested to clone both repositories as siblings,
   and to use PYTHONPATH. For example:

   .. CODE:: bash

      mkdir VUnit
      cd VUnit
      git clone -b cosim --recurse-submodules -j4 https://github.com/dbhi/vunit
      git clone https://github.com/vunit/cosim
      export PYTHONPATH="$(pwd)/vunit":"$(pwd)/cosim"

.. _examples:vhpidirect:

VHPIDIRECT
----------

.. toctree::
   :maxdepth: 2

   copy
   buffer
