The ifconfig Command
====================
.. currentmodule:: apcommand.commands.ifconfig
A module to query the device for interface information. Right now this is targeted at linux-devices other than androids (which have a different output). Although my real target is the Atheros AP which has busybox on it I do not have a device to test with so I am using my desktop output and assuming that it is the same as the AP.



.. _ifconfig-lexer:

The IfconfigLexer
-----------------

This is a tokenizer for `ifconfig` output.

.. autosummary::
   :toctree: api

   IfconfigLexer
   IfconfigLexer.mac_address




