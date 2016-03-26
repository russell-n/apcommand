The Main Atheros Module
=======================

This is the `main` module, it provides the entry-point for controlling the atheros AP when it is run at the command-line.

Use Case 1
----------

.. uml::

   User -> (Brings AP Up)

In the first case the user brings the Access Point up. For the default case (|atheros|) the command-line interface::

   apcontrol up

.. currentmodule:: apcommand.atheros_main
.. autosummary:: 
   :toctree: api

   enable_debugger
   main










