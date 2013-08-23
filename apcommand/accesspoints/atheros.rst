Atheros
=======
.. currentmodule:: apcommand.accesspoints.atheros
This is a module to hold controllers for Access Points with Atheros-based chipsets. It is based partially on :ref:`Aren's Code <arens-atheros>` and partially on the Atheros' shell scripts found in ``/etc/ath`` on the device.

The Line Logger
---------------

Several of the classes have ended up using this same method so I broke it out so they could share one source instead of duplicating the code.

.. uml

   LineLogger -|> BaseClass

.. autosummary::
   :toctree: api

   LineLogger



AtherosAR5KAP
-------------

This is an access-point used for WiFi Alliance testing. It is not a commercial access-point. The commands to control it are taken from the code that Aren :ref:`wrote <arens-atheros>`. The primary request was that I create a command-line command to change the AP-channel. As such it does not change settings en-masse the way that Arens code does, as it assumes that only incremental changes are being made.

.. uml::

   AtherosAR5KAP o- LineLogger
   AtherosAR5KAP o- AtherosChannelChanger
   AtherosAR5KAP o- ArbitraryCommand   
   AtherosAR5KAP -|> BaseClass

.. autosummary::
   :toctree: api

   AtherosAR5KAP
   


Atheros Security Setter
-----------------------

This is a base-class for the security setters.

.. uml::

   AtherosSecuritySetter -|> BaseClass
   AtherosSecuritySetter o- LineLogger
   AtherosSecuritySetter : __call__(type)

.. autosummary::
   :toctree: api

   AtherosSecuritySetter



AtherosOpen Security
--------------------

This sets the security to open-none.

.. uml::

   AtherosOpen -|> AtherosSecuritySetter

.. autosummary::
   :toctree: api

   AtherosOpen



AtherosChannelChanger
---------------------

.. uml::

   AtherosChannelChanger -|> BaseClass
   AtherosChannelChanger : __call__(channel, mode)

.. autosummary::
   :toctree: api

   AtherosChannelChanger

This was a base class for 2.4 and 5 ghz channel changers but I realized that the settings should be discovered through the channel that is being passed in so it does not make sense to maintain separate classes.



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
   TestAR5KAP.test_set_channel
   TestAR5KAP.test_set_security
   


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
   

.. autosummary::
   :toctree: api

   TestAtherosOpen.test_call
   






