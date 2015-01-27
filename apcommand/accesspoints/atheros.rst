Atheros
=======

This is a module to hold controllers for Access Points with Atheros-based chipsets. It is based partially on Aren's Code and partially on the Atheros' shell scripts found in ``/etc/ath`` on the device.

Contents:

   * :ref:`Line Logger <line-logger>`
   * :ref:`TheConfigure <the-configure>`
   * :ref:`AtherosAR5KAP <atheros-ar5kap>`
   * :ref:`AtherosSecuritySetter <atheros-security-setter>`
   * :ref:`AtherosOpen Security <atheros-open-security>`
   * :ref:`AtherosChannelChanger <atheros-channel-changer>`
   






.. _line-logger:

The Line Logger
---------------

Several of the classes have ended up using this same method so I broke it out so they could share one source instead of duplicating the code.

.. uml

   LineLogger -|> BaseClass

.. module:: apcommand.accesspoints.atheros
.. autosummary::
   :toctree: api

   LineLogger
   LineLogger.__call__




.. _the-configure:   

The Configure
-------------

The `Configure` is a `context manager <http://docs.python.org/release/2.5/whatsnew/pep-343.html>`_ for commands. It does not actually make use of all the exception handling that is a feature of context managers. Maybe next time.

.. uml::

   Configure -|> BaseClass
   Configure : __init__(connection)

.. autosummary::
   :toctree: api

   Configure
   Configure.__enter__
   Configure.__exit__





.. _atheros-ar5kap:

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
   AtherosAR5KAP.up
   AtherosAR5KAP.down
   AtherosAR5KAP.destroy
   AtherosAR5KAP.status
   AtherosAR5KAP.reset
   AtherosAR5KAP.set_ssid
   AtherosAR5KAP.set_ip
   AtherosAR5KAP.set_channel
   AtherosAR5KAP.set_security
   AtherosAR5KAP.exec_command
   




.. _atheros-security-setter:
   
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




.. _atheros-open-security:

AtherosOpen Security
--------------------

This sets the security to open-none.

.. uml::

   AtherosOpen -|> AtherosSecuritySetter

.. autosummary::
   :toctree: api

   AtherosOpen




.. autosummary::
   :toctree: api

   TestAtherosOpen.test_call

.. _atheros-channel-changer:
   
AtherosChannelChanger
---------------------

.. uml::

   AtherosChannelChanger -|> BaseClass
   AtherosChannelChanger o- SettingsValidator
   AtherosChannelChanger : __call__(channel, mode)   

.. autosummary::
   :toctree: api

   AtherosChannelChanger

This was a base class for 2.4 and 5 ghz channel changers but I realized that the settings should be discovered through the channel that is being passed in so it does not make sense to maintain separate classes.




Testing the AtherosAR5KAP
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api

   TestAR5KAP.test_constructor
   TestAR5KAP.test_up
   TestAR5KAP.test_down
   TestAR5KAP.test_destroy
   TestAR5KAP.test_status
   TestAR5KAP.test_ifconfig_fail
   TestAR5KAP.test_reset
   TestAR5KAP.test_set_ssid
   TestAR5KAP.test_set_channel_24
   TestAR5KAP.test_set_channel_5
   TestAR5KAP.test_set_security

.. autosummary::
   :toctree: api

   TestAtheros24.test_set_channel
   TestAtheros24.test_bandwidth
   TestAtheros24.test_parameter_suffix
   TestAtheros24.test_mode
   TestAtheros24.test_band   
   
.. autosummary::
   :toctree: api

   TestAtheros5GHz.test_band
   TestAtheros5GHz.test_bandwidth
   TestAtheros5GHz.test_parameter_suffix
   TestAtheros5GHz.test_mode
   TestAtheros5GHz.test_set_channel
   TestAtheros5GHz.test_validate_channel


.. autosummary::
   :toctree: api

   TestConfigure.test_constructor
   TestConfigure.test_enter
   TestConfigure.test_exit

   

















   



29.165.126.179
