Iwlist Lexer
============
.. currentmodule:: apcommand.commands.iwlist
A module to hold lexers for the `iwlist <http://en.wikipedia.org/wiki/Wireless_tools_for_Linux#iwlist>`_ command. I don't use it often so it won't have a lot to it initially.

This is modeled on the :ref:`IwconfigLexer <iwconfig-lexer>` but that was originally created to continuously poll information from a device and so bundles the command, connection and lexer into one class (it's much too big, it should get un-bundled at some point). In this case I'm creating something to search the output of lines given to it (hopefully the output of the `iwlist` command) and leave it up to the user to run the command on the connection and get the output to give to the `IwlistLexer`.

.. uml::

   IwlistLexer -|> BaseClass
   IwlistLexer : channel(lines)
   IwlistLexer : frequency(lines)

.. autosummary::
   :toctree: api

   IwlistLexer
   IwlistEnum

.. uml::

   IwlistCommand -|> BaseClass
   IwlistCommand o- IwlistLexer

.. autosummary::
   :toctree: api

   IwlistCommand
   









.. autosummary::
   :toctree: api

   TestIwlist.test_constructor
   TestIwlist.test_frequency_expression
   TestIwlist.test_frequency
   TestIwlist.test_channel_expression
   TestIwlist.test_channel
   









