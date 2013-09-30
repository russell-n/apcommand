The Broadcom Queriers
=====================
.. currentmodule:: apcommand.accesspoints.broadcom.querier
.. _broadcom-queriers:
In order to trim down the class-explosion that seems to be going on, all the querys to the Broadcom are combined into two classes :ref:`Broadcom5GHzQuerier <broadcom-5-ghz-querier>` and :ref:`Broadcom24GHzQuerier <broadcom-24-ghz-querier>`.

Contents:

    * :ref:`BroadcomBaseQuerier <broadcom-base-querier>`
    * :ref:`Broadcom24GHzQuerier <broadcom-24-ghz-querier>`
    * :ref:`Broadcom5GHzQuerier <broadcom-5-ghz-querier>`

The set_page Decorator
----------------------

Because I am trying to repeat calls to the server the set_page decorator differs from the one used by the commands. 



.. uml::

   BroadcomBaseQuerier -|> BaseClass
   BroadcomBaseQuerier o-- HTTPConnection
   BroadcomBaseQuerier o-- BroadcomRadioSoup
   BroadcomBaseQuerier : band   

.. _broadcom-base-querier:
BroadcomBaseQuerier
~~~~~~~~~~~~~~~~~~~

.. uml::

   BroadcomBaseQuerier -|> BaseClass
   BroadcomBaseQuerier : __init__(connection, [refresh)

.. autosummary::
   :toctree: api

   BroadcomBaseQuerier
   BroadcomBaseQuerier.channel
   BroadcomBaseQuerier.state
   BroadcomBaseQuerier.sideband
   BroadcomBaseQuerier.mac_address
   BroadcomBaseQuerier.ssid

The ``refresh`` parameter, if False (the default) will cause the Queriers to only pull a page if it is not already loaded, that way multiple checks will not incur the overhead of waiting for the server (and more significantly the sleeps after each call).



The Page Enumerations
---------------------

Since there are an arbitrary number of pages to add (assuming that not all are being used), they will be identified by an enumeration. If a page is added (i.e. it gets a ``set_<page>_soup`` method) then it should be added to the enumeration.

.. uml::

   PageEnumeration : ssid
   PageEnumeration : radio

The Refresh Parameter Revisited
-------------------------------

In the ``set_<page>_soup`` methods they should check both the ``refresh`` variable and the ``current_page`` to see if the desired page should be loaded, and if it is loaded, the ``current_page`` should be set to the appropriate ``PageEnumeration`` value (e.g. ``self.current_page = PageEnumeration.ssid``).

.. csv-table:: Set Soup Truth Table
   :header: ``refresh``,``current_page=PageEnumeration``, Set the Soup

   False, False, True
   False, True, False
   True, False, True
   True, True, True

As you can see from the truth table, there is only one case where you will not load the page -- :math:`\lnot (\lnot refresh \land current_page=enumeration)`, which can be re-written :math:`refresh \lor \lnot current_page=enumeration`. But, on reflection, it actually makes more sense to short-circuit the one case where we do nothing -- :math:`\lnot refresh \land current_page=enumeration`.



The BroadcomRadioQuerier
------------------------

This is a querier for the radio.asp page.

.. uml::

   BroadcomRadioQuerier -|> BroadcomBaseQuerier

.. autosummary::
   :toctree: api

   BroadcomRadioQuerier
   BroadcomRadioQuerier.mac_address
   BroadcomRadioQuerier.sideband
   BroadcomRadioQuerier.channel
   BroadcomRadioQuerier.state

Example to get the channel for each band::

    q = BroadcomRadioQuerier(connection=connection, band='2.4')
    channel_24 = q.channel

    q.band = 5
    channel_5 = q.channel    



The BroadcomSSIDQuerier
-----------------------

A querier for the ssid.asp page.

.. uml::

   BroadcomSSIDQuerier -|> BroadcomBaseQuerier

.. autosummary::
   :toctree: api

   BroadcomSSIDQuerier
   BroadcomSSIDQuerier.ssid



The BroadcomLANQuerier
----------------------

A querier for the ``lan.asp`` page.

.. uml::

   BroadcomLANQuerier -|> BroadcomBaseQuerier

.. autosummary::
   :toctree: api

   BroadcomLANQuerier
   BroadcomLANQuerier.dhcp_state




