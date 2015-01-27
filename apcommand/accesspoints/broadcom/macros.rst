Broadcom Macros
===============

Since the :ref:`commands <broadcom-commands>` have been broken down to do only one thing each (discounting the `undo` methods) in order to get more complex actions they need to be aggregated into what I'm loosely calling macros (the original intent was to use the Macro Pattern, but that isn't working out at the moment).




The ChannelChanger
--------------------------

.. uml::

   ChannelChanger -|> BaseClass

.. module:: apcommand.accesspoints.broadcom.macros
.. autosummary::
   :toctree: api

   ChannelChanger
   










