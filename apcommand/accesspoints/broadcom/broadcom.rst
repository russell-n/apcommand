The Broadcom BCM94718NR Access Point
====================================
.. currentmodule:: apcommand.accesspoints.broadcom.broadcom

The Broadcom advertises a telnet connection but it will not let you log in. To control it you will need to send commands to its web-page. Although something like `Selenium <http://docs.seleniumhq.org/>`_ should work, to simplify the control for the command line, a more containde method will be used. Aren used `curl <http://en.wikipedia.org/wiki/CURL>`_ to send commands to the Access Point.

Using `curl` introduces two problems:

   * Most distributions do not come with `curl` installed (not a big problem for linux/unix systems)

   * We now have an indirect communication to the access point, as the python code has to talk to a machine that talks to the access point


.. digraph:: curl_topology

   C -> V -> A

Where `C` is the `Control PC`, `V` is a `Ventriloquist PC` that uses `curl` to talk to `A`, the `Broadcom Access Point`. In the simplest case the Control PC could fork a sub-process or talk to its `localhost`:

.. digraph:: curl_back_topology

   C -> C
   C -> A

Still, the use of `curl` seems inelegant, so I will attempt to do it with the python standard library module `urllib2` and related modules.

.. note:: Right now I am trying out `requests <http://docs.python-requests.org/en/latest/>`_ (a replacement for `urllib2`) and `BeautifulSoup <http://www.crummy.com/software/BeautifulSoup/>`_ with regular expressions to read the html output.

.. note:: The broadcom needs time between calls -- if you try to access the web server too soon after a previous call to it might not respond or not respond correctly.

The BroadcomBCM94718NR (Henceforth to be known as 'George')
-----------------------------------------------------------

.. uml::

   BroadcomBCM94718NR -|> BaseClass
   BroadcomBCM94718NR o- HTTPConnection
   BroadcomBCM94718NR o- BroadcomChannelChanger

.. autosummary::
   :toctree: api

   BroadcomBCM94718NR
   BroadcomBCM94718NR.set_channel
   BroadcomBCM94718NR.get_channel
   BroadcomBCM94718NR.set_5_ssid
   BroadcomBCM94718NR.set_24_ssid
   
* See the :ref:`HTTPConnection <http-connection>` page for more on what it is about.



.. autosummary::
   :toctree: api

   radio_page
   ssid_page
   action_dict
   set_24_data
   set_5_data
   

.. autosummary::
   :toctree: api

   RadioPageConnection





[]
[]


