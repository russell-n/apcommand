The Firmware Page
=================

This is a module for getting information from the ``firmware.asp`` page. 


.. code:: python

    # python standard library
    import re
    
    # third-party
    from bs4 import BeautifulSoup
    
    # this package
    from apcommand.accesspoints.broadcom.parser import BroadcomBaseSoup
    from apcommand.accesspoints.broadcom.commons import BroadcomPages
    from apcommand.accesspoints.broadcom.querier import BroadcomBaseQuerier
    



The BroadcomFirmwareSoup
------------------------

Using the stuff from :ref:`Firmware Exploration <firmwares-exploration>`, a Soup for the information will be created.

.. uml::

   BroadcomFirmwareSoup -|> BroadcomBaseSoup

.. currentmodule:: apcommand.accesspoints.broadcom.firmware
.. autosummary::
   :toctree: api

   BroadcomFirmwareSoup
   BroadcomFirmwareSoup.bootloader_version
   BroadcomFirmwareSoup.os_version
   BroadcomFirmwareSoup.wl_driver_version






The FirmwareQuerier
-------------------

Now a querier to bundle the Soup with a connection

.. uml::

   BroadcomFirmwareQuerier -|> BroadcomBaseQuerier

.. currentmodule::    apcommand.accesspoints.broadcom.firmware
.. autosummary::

   BroadcomFirmwareQuerier








