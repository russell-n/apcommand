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
    SSID = 'wl_ssid'
    



BandEnum
--------

This is to try and make how 2.4 ghz is specified more consistent.

.. uml::

   BandEnumeration : two_point_four
   BandEnumeration : five



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
   BroadcomRadioData : control_channel



BroadcomLANData
~~~~~~~~~~~~~~~

This is data for the ``lan.asp`` page.

.. uml::

   BroadcomLANData : lan_page

::

    class BroadcomLANData(object):
        __slots__ = ()
        lan_page = 'lan.asp'
    



BroadcomWirelessData
~~~~~~~~~~~~~~~~~~~~

This holds settings for the `Wireless Interface` drop-down which decides which interface will be affected by changed settings. It is used on several pages so I pulled it out by itself.

.. uml::

    BroadcomWirelessData : wireless_interface
    BroadcomWirelessData : interface_5_ghz
    BroadcomWirelessData : interface_24_ghz



BroadcomPages
-------------

A holder of names of the web-pages.

.. uml::

   BroadcomPages : radio
   BroadcomPages : lan
   BroadcomPages : ssid
   BroadcomPages : firmware
   BroadcomPages : security



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
    
    # a decorato to set the page assuming that the object has a self.asp_page attribute
    def set_page(method):
        """
        Decorator: sets connection.path to self.asp_page before, sleeps after
        """
        def _method(self, *args, **kwargs):
            self.logger.debug("Setting connection.path to {0}".format(self.asp_page))
            self.connection.path = self.asp_page
            outcome = method(self, *args, **kwargs)
            return outcome
        return _method
    
    



Data
----



Errors
------

.. autosummary::
   :toctree: api

   BroadcomError

