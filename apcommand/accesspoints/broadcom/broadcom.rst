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

The BroadcomBCM94718NR
----------------------

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

   BroadcomError



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




The Broadcom Commands
---------------------

I have decided to break the commands sent to the Broadcom into atomic actions. If they are run separately this will actually make them inefficient time-wise, as you need to put about a half-second pause between each call to the server or it will occasionally not respond, but my guess is that I will not have access to the Broadcom again for a long while and like most things here this will turn into a code-maintenance nightmare. To ameliorate the knowledge-gain, knowledge-lost cycle that is common to projects here I am trying to make the code as simple as possible at the possible expense of execution efficiency. Of course, one could argue that an explosion of classes does not clarify anything but I am hopeful that once the pattern is recognized only the relevant classes need be found and examined and so smaller will be better.

To allow for the aggregation of commands each command class has an `add` method which will allow other commands to be added to their data-dictionary. This way the `Apply` action only needs to be called once per page. There are too many things on the pages for me to check if they make sense, though, so user-beware.

A hypothetical example::

   connection = HTTPConnection('192.168.1.1', password='admin', path='radio.asp')
   command = Set24GHzChannel(connection)
   other_command = Disable5GHz(connection)
   command += other_command
   command('11')

.. autosummary::
   :toctree: api

   BroadcomBaseCommand



.. autosummary::
   :toctree: api

   Base5GHzCommand



.. uml::

   BroadcomChannelChanger -|> BaseClass

.. autosummary::
   :toctree: api

   BroadcomChannelChanger
   



.. autosummary::
   :toctree: api

   BroadcomChannelReader


[]
[]


