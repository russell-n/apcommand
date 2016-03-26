Atheros
=======

This is a module to hold controllers for Access Points with Atheros-based chipsets. It is based on the Atheros' shell scripts found in ``/etc/ath`` on one Atheros device.

.. '
   



Constants
---------


.. code:: python

    EMPTY_STRING = ''
    FIVE_GHZ_SUFFIX = '_2'
    
    TWO_POINT_FOUR = '2.4'
    FIVE = '5'
    BAND_ID = {TWO_POINT_FOUR:0, FIVE:1}
    G_BANDWIDTH = 'HT20'
    A_LOWER_BANDWIDTH = 'HT40PLUS'
    A_UPPER_BANDWIDTH = 'HT40MINUS'
    



Imported Classes
----------------

The Atheros classes make use of some imported classes. Rather than re-document them here I'll just provide the relevant autosummary documentation.

.. '

.. currentmodule::  apcommand.baseclass
.. autosummary::
   :toctree: api

   BaseClass

.. currentmodule:: apcommand.connections.telnetconnection
.. autosummary::
   :toctree: api
   
   TelnetConnection

.. currentmodule:: apcommand.commons.errors
.. autosummary::
   :toctree: api

   CommandError

.. currentmodule:: apcommand.commons.errors
.. autosummary::
   :toctree: api

   ArgumentError

.. currentmodule:: apcommand.accesspoints.arbitrarycommand
.. autosummary::
   :toctree: api
   
   ArbitraryCommand

.. currentmodule:: apcommand.commands.settingsvalidator
.. autosummary::
   :toctree: api

   SettingsValidator


.. _line-logger:

The Line Logger
---------------

Several of the classes have ended up using this same logging method so I broke it out so they could share one source instead of duplicating the code.

.. uml::

   BaseClass <|-- LineLogger
   LineLogger o- CommandError
   LineLogger o- logging.Logger

.. module:: apcommand.accesspoints.atheros
.. autosummary::
   :toctree: api

   LineLogger
   LineLogger.__call__

The :ref:`BaseClass <base-class>` provides the actual logger, this allows the log-level to be changed on the fly and strips the line-endings off to get rid of extra blank lines in the log.




.. _the-configure:   

The Configure
-------------

The `Configure` is a `context manager <http://docs.python.org/release/2.5/whatsnew/pep-343.html>`_ for commands. It does not actually make use of all the exception handling that is a feature of context managers. Maybe next time.

.. uml::

   BaseClass <|-- Configure
   Configure o- LineLogger
   Configure : __init__(connection)

.. autosummary::
   :toctree: api

   Configure
   Configure.__enter__
   Configure.__exit__





.. _atheros-ar5kap:

AtherosAR5KAP
-------------

This is an access-point used for WiFi Alliance testing. It is not a commercial access-point. The primary request was that I create a command-line command to change the AP-channel. As such it does not change settings en-masse, as it assumes that only incremental changes are being made.

.. uml::

   BaseClass <|-- AtherosAR5KAP
   AtherosAR5KAP o- LineLogger
   AtherosAR5KAP o- AtherosChannelChanger
   AtherosAR5KAP o- ArbitraryCommand
   AtherosAR5KAP o- TelnetConnection


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


   BaseClass <|-- AtherosSecuritySetter
   AtherosSecuritySetter o- LineLogger
   AtherosSecuritySetter : __call__(type)

.. autosummary::
   :toctree: api

   AtherosSecuritySetter
   AtherosSecuritySetter.__call__




.. _atheros-open-security:

AtherosOpen Security
--------------------

This sets the security to open-none.

.. uml::

   AtherosSecuritySetter <|-- AtherosOpen

.. autosummary::
   :toctree: api

   AtherosOpen
   AtherosOpen.__call__




Testing the Atheros Open
~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api

   TestAtherosOpen.test_call

.. _atheros-channel-changer:
   
AtherosChannelChanger
---------------------

.. uml::

   BaseClass <|-- AtherosChannelChanger
   AtherosChannelChanger o- SettingsValidator
   AtherosChannelChanger o- LineLogger
   AtherosChannelChanger : __call__(channel, mode)   

.. autosummary::
   :toctree: api

   AtherosChannelChanger
   AtherosChannelChanger.channels
   AtherosChannelChanger.g_channels
   AtherosChannelChanger.a_channels
   AtherosChannelChanger.a_lower_channels
   AtherosChannelChanger.a_upper_channels
   AtherosChannelChanger.channel_to_bandwidth
   AtherosChannelChanger.a_channels_mode_map
   AtherosChannelChanger.bandwidth
   AtherosChannelChanger.mode
   AtherosChannelChanger.band
   AtherosChannelChanger.__call__
   AtherosChannelChanger.validate_channel

This was originally a base class for 2.4 and 5 ghz channel changers but I realized that the settings should be discovered through the channel that is being passed in so it does not make sense to maintain separate classes.




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

   

















   






