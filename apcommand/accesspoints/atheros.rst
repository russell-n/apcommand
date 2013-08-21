Atheros
=======
.. currentmodule:: apcommand.accesspoints.atheros
This is a module to hold controllers for Access Points with Atheros-based chipsets.

AtherosAR5KAP
-------------

This is an access-point used for WiFi Alliance testing. It is not a commercial access-point. The commands to control it are taken from the code that Aren :ref:`wrote <arens-atheros>`. The primary request was that I create a command-line command to change the AP-channel. As such it does not change settings en-masse the way that Arens code does, as it assumes that only incremental changes are being made.

.. autosummary::
   :toctree: api

   AtherosAR5KAP



AtherosChannelChanger
---------------------

This is a base-class for the Atheros 2.4 GHz and Atheros 5 Ghz channel changers to inherit from.



Atheros24
---------

The channel setting commands are slightly different for the 2.4 GHz and 5GHz radios so to make it a little simpler they are separated out.

.. uml::

   Atheros24 -|> AtherosChannelChanger
   Atheros24 : set_channel(channel)

.. autosummary::
   :toctree: api

   Atheros24Ghz



Atheros5
--------

This is the countepart to the `Atheros24` for 5 Ghz.

.. uml::

   Atheros5GHz -|> AtherosChannelChanger
   Atheros5GHz : set_channel(channel)

.. autosummary::
   :toctree: api

   Atheros5GHz





.. autosummary::
   :toctree: api

   TestAR5KAP.test_constructor
   TestAR5KAP.test_up
   TestAR5KAP.test_down
   TestAR5KAP.test_destroy
   TestAR5KAP.test_status
   TestAR5KAP.test_reset
   


The Configure
-------------

The `Configure` is a `context manager <http://docs.python.org/release/2.5/whatsnew/pep-343.html>`_ for commands. It does not actually make use of all the exception handling that is a feature of context managers, mostly because this is a rush job and I do not have time to try and make this robust. Maybe next time.

.. uml::

   Configure -|> BaseClass
   Configure : __init__(connection)

.. autosummary::
   :toctree: api

   Configure.__enter__
   Configure.__exit__



.. autosummary::
   :toctree: api

   TestConfigure.test_constructor
   TestConfigure.test_enter
   TestConfigure.test_exit
   TestConfigure.test_other_interface
   TestConfigure.test_radio_id



.. autosummary::
   :toctree: api

   TestAtheros24.test_set_channel
   







