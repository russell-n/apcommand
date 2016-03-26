The Argument Parser
===================

A map from command-line-arguments to a namespace.

.. uml::

   Arguments o- argparse.ArgumentParser
   Arguments o- subcommands.SubCommand
   Arguments : argparse.namespace arguments

.. currentmodule:: apcommand.broadcom.argumentparser
.. autosummary::
   :toctree: api

   Arguments
   Arguments.subcommands
   Arguments.parser
   Arguments.arguments
   Arguments.subparsers
   Arguments.add_arguments
   Arguments.add_subparsers

Since the hostname changes around I added a `fromfile_prefix_chars=@` to the ArgumentParser so you can put the argument (``--hostname=192.168.30.22`` **Not strings, type exactly what you would type on the command-line**) in a file then pass them in like::

   broadcom @config.txt status





