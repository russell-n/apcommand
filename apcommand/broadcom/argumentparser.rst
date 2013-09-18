The Argument Parser
===================
.. currentmodule:: apcommand.Broadcom.argumentparser
A map from command-line-arguments to a namespace.

.. uml::

   Arguments o- argparse.ArgumentParser
   Arguments o- subcommands.SubCommand
   Arguments : argparse.namespace arguments

.. autosummary::
   :toctree: api

   Arguments

