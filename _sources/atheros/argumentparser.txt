The Argument Parser
===================
.. currentmodule:: apcommand.argumentparser
A map from command-line-arguments to a namespace.

.. uml::

   Arguments o- argparse.ArgumentParser
   Arguments o- subcommands.SubCommand
   Arguments : argparse.namespace arguments

.. currentmodule:: apcommand.atheros.argumentparser   
.. autosummary::
   :toctree: api

   Arguments
   Arguments.subcommands
   Arguments.parser
   Arguments.subparsers
   Arguments.add_arguments
   Arguments.add_subparsers





