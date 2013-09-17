Arens Atheros Code
==================

.. currentmodule:: apcommand.arenscode.arensatheros

.. _arens-atheros:

This is the code that aren wrote following the coding style of Lab126. It will be used as the reference for the AP Command.

.. uml::

   Atheros o- Serial

.. autosummary::
   :toctree: api

   Atheros

Configuring the 2.4 GHz Interface
---------------------------------

The command line sequence::

    apdown
    cfg -x
    cfg -a AP_CHMODE=<mode>HT20
    cfg -a AP_PRIMARY_CH=<channel>
    cfg -a AP_STARTMODE=standard
    cfg -a AP_RADIO_ID=0
    cfg -a AP_SSID=<ssid>
    iwconfig ath0 rts <rts>
    iwconfig ath0 frag <framentation>
    cfg -c
    apup

* mode is one of (11na, 11ng, 11a, or 11g)

Configuring the 5GHz Setup
--------------------------

The command-line sequence::

    apdown
    cfg -x
    cfg -a AP_CHMODE_2=<mode>HT20
    cfg -a AP_PRIMARY_CH_2=<channel>
    cfg -a AP_STARTMODE=standard
    cfg -a AP_RADIO_ID=1
    cfg -a AP_SSID=<ssid>
    iwconfig ath0 rts <rts>
    iwconfig ath0 frag <framentation>
    cfg -c
    apup
   
