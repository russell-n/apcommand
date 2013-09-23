The Broadcom Commons
====================
.. currentmodule:: apcommand.accesspoints.broadcom.commons

To prevent circular imports common methods, functions, and constants are put in here (or maybe they are put in here to prevent circular imports, whichever you prefer).


Constants
---------

Some of the constants are gathered into a class in order to try and make it easier to understand what they refer to. In particular the data names and values (e.g. 'wl_unit' and '0') are grouped by page.

::

    ZERO = '0'
    ONE = '1'
    
    SSID_PAGE = 'ssid.asp'
    
    CONTROL_CHANNEL = 'wl_channel'
    SIDEBAND = 'wl_nctrlsb'
    SSID = 'wl_ssid'
    



BroadcomRadioData
~~~~~~~~~~~~~~~~~

This holds constants for the radio.asp page.

.. uml::

   BroadcomRadioData : channels_24ghz
   BroadcomRadioData : channels_5ghz
   BroadcomRadioData : interface
   BroadcomRadioData : radio_page
   BroadcomRadioData : radio_on
   BroadcomRadioData : radio_off



BroadcomWirelessData
~~~~~~~~~~~~~~~~~~~~

This holds settings for the `Wireless Interface` drop-down which decides which interface will be affected by changed settings. It is used on several pages so I pulled it out by itself.

.. uml::

    BroadcomWirelessData : wireless_interface
    BroadcomWirelessData : interface_5_ghz
    BroadcomWirelessData : interface_24_ghz



Decorators
----------

These are decorators to do the repetitive calls common to many methods.

.. autosummary::
   :toctree: api

   radio_page
   ssid_page

::

    # a decorator to set the page to 'radio.asp'
    def radio_page(method):
        """
        Decorator: sets connection.path to radio.asp before, sleeps after
        """
        def _method(self, *args, **kwargs):
            self.logger.debug("Setting connection.path to '{0}'".format(BroadcomRadioData.radio_page))
            self.connection.path = BroadcomRadioData.radio_page
            outcome = method(self, *args, **kwargs)
            return outcome
        return _method
    
    # a decorator to set the page to 'ssid.asp'
    def ssid_page(method):
        """
        Decorator: sets connection.path to ssid.page before, sleeps after
        """
        def _method(self, *args, **kwargs):
            self.logger.debug("Setting connection.path to {0}".format(SSID_PAGE))
            self.connection.path = SSID_PAGE
            outcome = method(self, *args, **kwargs)
            return outcome
        return _method
    



Data
----

