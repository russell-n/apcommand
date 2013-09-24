The Broadcom Commands
=====================

.. currentmodule: apcommand.accesspoints.broadcom.broadcom_commands

Contents:

   * :ref:`Introduction <broadcom-commands-introduction>`
   * :ref:`BroadcomBaseData <broadcom-base-data>`

   * :ref:`BroadcomBaseCommand <broadcom-base-command>`


.. _broadcom-commands-introduction:
Introduction
------------

I have decided to break the commands sent to the Broadcom into atomic actions. If they are run separately this will actually make them inefficient time-wise, as you need to put about a half-second pause between each call to the server or it will occasionally not respond, but my guess is that I will not have access to the Broadcom again for a long while and like most things here this will turn into a code-maintenance nightmare. To ameliorate the knowledge-gain, knowledge-lost cycle  I am trying to make the code as simple as possible at the possible expense of execution efficiency. Of course, one could argue that an explosion of classes does not simplify anything but I am hopeful that once the pattern of implementation is recognized only the relevant classes need be found and examined and so smaller will be better.

To allow for the aggregation of commands each command class has an `add` method which will allow other commands to be added to their data-dictionary. This way the `Apply` action only needs to be called once per page. There are too many things on the pages for me to check if they make sense, though, so user-beware.

A hypothetical example::

   connection = HTTPConnection('192.168.1.1', password='admin', path='radio.asp')
   set_channel = Set24GHzChannel(connection)
   disable = Disable5GHz(connection)
   set_channel += disable
   set_channel('11')

This should have the equivalent effect of::

    set_channnel('11')
    disable()

But since the first case only accesses the server once it should be faster. Also, if for some reason you want to remove the ``disable`` data from the ``set_channel`` data you can use::

    set_channel -= disable

In this case it would probably be better to re-create the ``set_channel``, but conceivably you could chain together many commands and there might be a reason to remove just one part of it.

.. _broadcom-base-data:
The Base Data
-------------

A *command* is data sent to the server. At a minimum the server is sent the interface information as data so that the :ref:`Soup <broadcom-radio-soup>` can find values in the html. The Base Data classes hold the Wireless Interface data for the specific bands. I was going to create it as a real class so it could be re-used but I think it makes more sense for the commands to use it once and throw it away so it is created with classmethods so that the actual object does not have to be created (although it can be if needed). I still have not quite worked out the logic of how this all fits together.

.. uml::

   BroadcomBaseData -|> BaseClass

.. autosummary::
   :toctree: api

   BroadcomBaseData
   BroadcomBaseData.base_data
   BroadcomBaseData.base_24_ghz_data
   BroadcomBaseData.base_5_ghz_data




.. _broadcom-base-command:
The Broadcom Base Command
-------------------------

As mentioned above, a `command` is a bundle of data to send to the web-server and the connection to send it over. The assumption is that there will be 6 cases to build the BaseCommand -- cases where no data is sent, cases where an interface has to be chosen but no action, cases with an interface and an action, and cases with an action but no interface. An action has to be sent if something is being changed, but should not be sent just to read the html. An interface needs to be chosen for pages dealing with wireless, but not for some of the pages not specific to wireless (e.g. the `LAN` page).

The data-dictionaries that need to be built will then meet the following cases (0 mean does not have this data, 1 mean has this data):

.. csv-table:: Base Data Dictionaries
   :header: Action,2.4 GHz,5 GHz

   0,0,0
   0,0,1
   0,1,0
   1,0,0
   1,0,1
   1,1,0

There are six rather than eight cases because you can only choose one Interface from the drop-down menu, not both.   

.. uml::

   BroadcomBaseCommand -|> BaseClass
   BroadcomBaseCommand o- HTTPConnection

.. autosummary::
   :toctree: api

   BroadcomBaseCommand
   BroadcomBaseData.base_data
   BroadcomBaseData.singular_data
   BroadcomBaseData.added_data
   BroadcomBaseData.non_base_data
   BroadcomBaseData.data
   BroadcomBaseData.__add__
   BroadcomBaseData.__sub__

This is getting a little convoluted so I will try and explain the data-dictionaries:

   * ``base_data``: this is set based on the band and action parameters and never changes
   * ``singular_data``: This is data added for a specific command to change settings
   * ``added_data``: this will be changed by the add and subtract operators
   * ``non_base_data``: this is ``singular_data`` updated by ``added_data``
   * ``data``: this is ``base_data`` updated by ``non_base_data``

The reason for all these data-dictionaries is so that commands can be composed from other commands. ``base_data`` and ``singular_data`` are part of the command-definition and so never change. ``non_base_data`` and ``data`` are generated every time ``added_data`` is changed (using the operators, if the ``added_data`` is changed directly then ``data`` and ``non_base_data`` will need to be reset). Only ``added_data`` is intended to change, and it is only changed using the other command's ``non_base_data`` so it will not change the original's Wireless Interface.




Enable Interface
----------------

This is a command implementation to enable the wireless interface.

.. uml::

   EnableInterface -|> BroadcomBaseCommand

.. autosummary::
   :toctree: api

   EnableInterface
   EnableInterface.__call__
   EnableInterface.singular_data
   EnableInterface.enable_5_data
   EnableInterface.enable_24_data



Disable Interface
~~~~~~~~~~~~~~~~~

This is a command implementation to disable a wireless interface.

.. uml::

   DisableInterface -|> BroadcomBaseCommand

.. autosummary::
   :toctree: api

   DisableInterface
   DisableInterface.__call__
   DisableInterface.singular_data
   DisableInterface.enable_5_data
   DisableInterface.enable_24_data



The Channel Setter
------------------

This is an implementation of a channel setter for the AP.

.. uml::

   SetChannel -|> BroadcomBaseCommand

.. autosummary::
   :toctree: api

   SetChannel



Set Sideband
------------

Sets the sideband -- assumes that it has to be 5GHz.

.. uml::

   SetSideband -|> BroadcomBaseCommand

.. autosummary::
   :toctree: api

   SetSideband




