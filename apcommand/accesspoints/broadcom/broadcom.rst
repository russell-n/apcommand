The Broadcom BCM94718NR Access Point
====================================

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

The BroadcomBCM94718NR
----------------------

.. uml::

   BroadcomBCM94718NR -|> BaseClass
   BroadcomBCM94718NR o- HTTPConnection
   BroadcomBCM94718NR o- BroadcomRadioSoup
   BroadcomBCM94718NR : enable_24_ghz
   BroadcomBCM94718NR : enable_5_ghz


[]
[]





