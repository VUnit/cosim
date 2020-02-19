.. _examples:copy:

Copy
######

This example shows the most basic usage of :class:`cosim.vhpidirect.VHPIDIRECT` (see :ref:`bridges:vhpidirect`) to interact with VUnit's internal ``string_ptr``/``byte_vector_ptr`` (see :ref:`vunit:data_types_library`) from C. :func:`cosim.vhpidirect.VHPIDIRECT.bridge` is used enable external mode support for ``string_ptr``. Two equivalent testbenches are provided: one uses ``string_ptr`` and the other one ``byte_vector_ptr``.
