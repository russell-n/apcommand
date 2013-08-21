The Sub-Commands
================
.. currentmodule:: apcommand.subcommands
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

   * AtherosAR5KAP

.. uml::

   SubCommand o- AtherosAR5KAP

.. autosummary::
   :toctree: api

   SubCommand -|> BaseClass
   SubCommand.up
   SubCommand.down
   SubCommand.destroy   




Testing The SubCommand
----------------------

The sub-command is largely ignorant of what the objects it holds does so this is mainly to check that the methods exist and if called will catch exceptions.

.. autosummary::
   :toctree: api

   TestSubCommand.test_up
   TestSubCommand.test_down
   TestSubCommand.test_destroy
   TestSubCommand.test_constructor
   TestSubCommand.test_args
   TestSubCommand.test_status
   TestSubCommand.test_security





