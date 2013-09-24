The Sub-Commands
================
.. currentmodule:: apcommand.broadcom.subcommands
This module holds the sub-commands for the Arguments (methods that it will call).

The try-except Decorator
------------------------

Since this is a user-level class (it is part of the command-line interface), exceptions are caught and logged, rather than allowing the interpreter to dump the stack-trace (it still logs and displays the stack-trace). To make this simpler a decorator is used to catch `Exception`.

.. autosummary::
   :toctree: api

   try_except
   


Class SubCommand
----------------

Role: Holds the sub-commands for the Arguments (the methods to actually call base on what the user passed in).

Collaborators:

   * Broadcom 

.. uml::

   SubCommand o- Broadcom

.. autosummary::
   :toctree: api

   SubCommand -|> BaseClass
   SubCommand.access_point
   SubCommand.status
   SubCommand.reset
   SubCommand.channel
   SubCommand.ssid
   SubCommand.security
   SubCommand.command
   SubCommand.ipaddress

