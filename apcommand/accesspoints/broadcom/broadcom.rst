The Broadcom BCM94718NR Access Point
====================================

The Broadcom advertises a telnet connection but it will not let you log in. To control it you will need to send commands to its web-page. Although something like `Selenium <http://docs.seleniumhq.org/>`_ should work, to simplify the control for the command line, a more contained method will be used. One way to control it would be to use `curl <http://en.wikipedia.org/wiki/CURL>`_ to send commands to the Access Point.

Using `curl` introduces two problems:

   * Most distributions do not come with `curl` installed (not a big problem for linux/unix systems)

   * We now have indirect communication to the access point, as the python code has to talk to a machine that talks to the access point


.. digraph:: curl_topology

   C -> V -> A

Where `C` is the `Control PC`, `V` is a `Ventriloquist PC` that uses `curl` to talk to `A`, the `Broadcom Access Point`. In the simplest case the Control PC could fork a sub-process or talk to its `localhost`:

.. digraph:: curl_back_topology

   C -> C
   C -> A

Still, the use of `curl` seems inelegant, so I will attempt to do it with the python standard library module `urllib2` and related modules.

.. note:: Right now I am trying out `requests <http://docs.python-requests.org/en/latest/>`_ (a replacement for `urllib2`) and `BeautifulSoup <http://www.crummy.com/software/BeautifulSoup/>`_ with regular expressions to read the html output.

.. note:: The broadcom needs time between calls -- if you try to access the web server too soon after a previous call to it might not respond or not respond correctly.







Aggregates
----------

These are parts taken from elsewhere in the code that are used in this module.

.. currentmodule:: apcommand.accesspoints.broadcom.commons
.. autosummary::
   :toctree: api
   
   BroadcomRadioData
   
.. currentmodule:: apcommand.accesspoints.broadcom.commons
.. autosummary::
   :toctree: api
   
   BandEnumeration

.. currentmodule::   apcommand.accesspoints.broadcom.querier
.. autosummary::
   :toctree: api

   BroadcomRadioQuerier
   BroadcomSSIDQuerier

.. currentmodule::  apcommand.accesspoints.broadcom.querier
.. autosummary::
   :toctree: api

   BroadcomLANQuerier

.. currentmodule::  apcommand.accesspoints.broadcom.firmware
.. autosummary::
   :toctree: api
   
   BroadcomFirmwareQuerier

.. currentmodule:: apcommand.accesspoints.broadcom.macros
.. autosummary::
   :toctree: api
   
   ChannelChanger

.. currentmodule::  apcommand.accesspoints.broadcom.commands
.. autosummary::
   :toctree: api

   DisableInterface

.. currentmodule:: apcommand.accesspoints.broadcom.commands
.. autosummary::
   :toctree: api

   EnableInterface

RadioPageConnection
-------------------

The `RadioPageConnection` is a context manager for the Broadcom controllers.

.. currentmodule:: apcommand.accesspoints.broadcom.broadcom
.. autosummary::
   :toctree: api

   RadioPageConnection
   RadioPageConnection.__enter__
   RadioPageConnection.__exit__





The BroadcomBCM94718NR
----------------------

.. uml::

   BaseClass <|-- BroadcomBCM94718NR
   BroadcomBCM94718NR o- HTTPConnection
   BroadcomBCM94718NR o- BroadcomChannelChanger
   BroadcomBCM94718NR o- BroadcomFirmwareQuerier
   BroadcomBCM94718NR o- BroadcomLANQuerier
   BroadcomBCM94718NR o- BroadcomRadioQuerier
   BroadcomBCM94718NR o- BroadcomSSIDQuerier
   BroadcomBCM94718NR o- EnableInterface
   BroadcomBCM94718NR o- DisableInterface
   BroadcomBCM94718NR o- ChannelChanger
   

.. currentmodule:: apcommand.accesspoints.broadcom.broadcom
.. autosummary::
   :toctree: api

   BroadcomBCM94718NR
   BroadcomBCM94718NR.set_channel
   BroadcomBCM94718NR.get_channel
   BroadcomBCM94718NR.set_5_ssid
   BroadcomBCM94718NR.set_24_ssid
   BroadcomBCM94718NR.firmware_query
   BroadcomBCM94718NR.lan_query
   BroadcomBCM94718NR.disable_command
   BroadcomBCM94718NR.enable_command
   BroadcomBCM94718NR.channel_changer
   BroadcomBCM94718NR.query
   BroadcomBCM94718NR.ssid_query
   BroadcomBCM94718NR.connection
   BroadcomBCM94718NR.set_5_ssid
   BroadcomBCM94718NR.set_24_ssid
   BroadcomBCM94718NR.get_ssid
   BroadcomBCM94718NR.set_channel
   BroadcomBCM94718NR.get_channel
   BroadcomBCM94718NR.print_and_log
   BroadcomBCM94718NR.get_status
   BroadcomBCM94718NR.log_status
   BroadcomBCM94718NR.unset_channel
   BroadcomBCM94718NR.disable
   BroadcomBCM94718NR.enable
   
   
* See the :ref:`HTTPConnection <http-connection>` page for more on what it is about.




