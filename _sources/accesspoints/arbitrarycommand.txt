Arbitrary Command
=================
.. currentmodule:: apcommand.accesspoints.arbitrarycommand
This takes an arbitrary command and sends it to the connection.

.. uml::

   ArbitraryCommand -|> BaseClass
   ArbitraryCommand : exec_command(command)

.. autosummary::
   :toctree: api

   ArbitraryCommand


.. autosummary::
   :toctree: api

   TestArbitraryCommand.test_constructor
   TestArbitraryCommand.test_call




