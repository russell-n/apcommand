The Iwconfig Command and Lexer
==============================
.. currentmodule:: apcommand.commands.iwconfig
A module to extract information from `iwconfig <http://en.wikipedia.org/wiki/Wireless_tools_for_Linux#iwconfig>`_.

In order to make the classes smaller and create a class that can parse Iwconfig output without bundling it with a connection to get the output I broke out the regular expressions out into a class :ref:`IwconfigLexer <iwconfig-lexer>`. Currently there is an awkward tie-in between the :ref:`IwconfigCommand <iwconfig-command>` and the lexer wherein the command is calling the IwconfigLexer.search method and passing in the lines, name and regular expression. This was done to avoid having a method for every expression but now the user of the lexer has to bundle together both its search method and one of its expressions as well as the name used in creating the regular expression. This seems like it requires too much knowledge about the internal workings of the Lexer, but the only alteranative I could come up with was creating extra methods. This should be unbundled later.





.. _iwconfig-enums:



.. _iwconfig-command:

.. autosummary::
   :toctree: api

   IwconfigCommand
   IwconfigEnums

.. uml::

   IwconfigCommand o- IwconfigLexer
   


.. _iwconfig-lexer:

.. autosummary::
   :toctree: api

   IwconfigLexer
   



.. autosummary::
   :toctree: api

   IwconfigLexer
   IwconfigEnums

.. uml::

   IwconfigLexer o- Connection
   IwconfigLexer : found_interface
   IwconfigLexer : protocol
   IwconfigLexer : frequency
   IwconfigLexer : bitrate
   IwconfigLexer : noise
   IwconfigLexer : rssi
   IwconfigLexer : ssid
   IwconfigLexer : bssid

.. autosummary::
   :toctree: api

   TestIwconfig.test_constructor
   TestIwconfig.test_bitrate
   TestIwconfig.test_ssid
   TestIwconfig.test_rssi
   TestIwconfig.test_noise
   TestIwconfig.test_bssid
   TestIwconfig.test_frequency
   TestIwconfig.test_protocol
   TestIwconfig.test_interface










