The Sub-Commands
================
.. currentmodule:: apcommand.subcommands
This module holds the sub-commands for the Arguments (methods that it will call).

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



Testing The SubCommand
----------------------

The sub-command is largely ignorant of what the objects it holds does so this is mainly to check that the methods exist and if called will catch exceptions.

.. autosummary::
   :toctree: api

   TestSubCommand.test_up
   TestSubCommand.test_constructor
   TestSubCommand.test_args





