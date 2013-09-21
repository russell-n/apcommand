The Broadcom Commands
=====================

.. currentmodule: apcommand.accesspoints.broadcom.broadcom_commands

Contents:

   * :ref:`Introduction <broadcom-commands-introduction>`
   * :ref:`BroadcomBaseData <broadcom-base-data>`

   * :ref:`BroadcomBaseCommand <broadcom-base-command>`
   * :ref:`Base5GHzCommand <base-5ghz-command>`
   


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
   BroadcomBaseData.base_24_ghz_data
   BroadcomBaseData.base_5_ghz_data




.. _broadcom-base-command:
The Broadcom Base Command
-------------------------

As mentioned above, a `command` is a bundle of data to send to the web-server and the connection to send it over. The base-command is abstract as the `base_data` attribute it has needs to be specific to the wireless interface being used (it holds either a :ref:`Base5GHzData <base-5ghz-data>` or :ref:`Base24GHzData <base-24ghz-data>` object).

.. uml::

   BroadcomBaseCommand -|> BaseClass
   BroadcomBaseCommand <|- Base5GHzCommand
   BroadcomBaseCommand <|- Base24GHzCommand
   BroadcomBaseCommand o- HTTPConnection

.. autosummary::
   :toctree: api

   BroadcomBaseCommand



.. _base-5ghz-command:

Base5GHzCommand
~~~~~~~~~~~~~~~




