The Broadcom Command Line
=========================

This is a description of the *broadcom* command that is created when this code is installed. All the commands are issued from a PC that has network-access to the Access Point.

.. _broadcom-command-line-interface:

The `Broadcom BCM94718NR GigE 802.11n Simultaneous Dual Band Router` controller is accessed at the command line via the ``broadcom`` command. A refresher can be pulled up using the ``broadcom -h`` option:




.. code::

    usage: broadcom [-h] [--pudb] [--pdb] [-s] [-d] [--hostname HOSTNAME]
                    [--username USERNAME] [--password PASSWORD] [--sleep SLEEP]
                    {status,channel,disable,enable,ssid} ...
    
    optional arguments:
      -h, --help            show this help message and exit
      --pudb                Run the `pudb` debugger (default=False).
      --pdb                 Run the `pdb` debugger (default=False).
      -s, --silent          If True only emit error messages (default=False)
      -d, --debug           If True emit debug messages (default=False)
      --hostname HOSTNAME   The hostname for the AP (leave unset for default).
      --username USERNAME   The user-login for the AP (leave unset for default)
      --password PASSWORD   The login password for the AP (Leave unset for
                            default)
      --sleep SLEEP         Seconds to sleep after web server call (default=0.5)
    
    Broadcom subcommands:
      Available Sub-Commands
    
      {status,channel,disable,enable,ssid}
                            Broadcom sub-commands
        status              Get some information for an interface
        channel             Change the AP channel
        disable             Disable a wireless interface.
        enable              Enable an interface.
        ssid                Change the SSID
    



The Initial Arguments
---------------------

Most of the initial arguments use the defaults for the router so if you haven't changed them you don't need to pass them in. The most likely thing to do is change the `hostname` (IP Address). For instance::

    broadcom --hostname 192.168.30.23

The sleep option
~~~~~~~~~~~~~~~~

The ``sleep`` option is there because the broadcom is being controlled via its web-interface and the web-server cannot take requests too soon after making a change. The ``sleep`` is thus a minimum amount of time that the program has to wait between page requests. If you make it too short it might return a socket error and abort (I could trap this but it could return a socket error for other reasons too so I thought it was better to give feedback). If you make it too long it might make the command take a long time but it should still work. The commands that query the AP for information require the least amount of sleeping (the ``status`` subcommand seems to get by with 0 sleep) but the sub-commands that change more than one thing (e.g. if you enable both radios) need at least a little sleep or you will probably get an error (I don't think it's the server-response-time so much as the saving of the data after a change is applied).

.. note:: These initial options are meant for the ``broadcom`` command and so have to come before any sub-commands (sub-commands are described below).

The general syntax for the ``broadcom`` command::

    broadcom <options> <sub-command> <sub-command options>

The Status Subcommand
---------------------

The ``status`` gets different state information for the router. The ``broadcom status --help``:


.. code::

    usage: broadcom status [-h] [band]
    
    positional arguments:
      band        the band of the interface to query (default=both)
    
    optional arguments:
      -h, --help  show this help message and exit
    
    



If you do not specify a band you should see something like::

    broadcom status
    
    2.4 GHz:
        Channel: 6
        SSID: pokerface
        State: Disabled
    5 GHz:
        Channel: 157
        SSID: hownowbrowndog
        State: Enabled
        Sideband: Lower
        
    DHCP: Disabled
    Bootloader Version: CFE 5.10.128.2
    OS Version: Linux  5.70.63.1
    WL Driver Version: 5.60.134

It also logs the information to the ``apcommand.log`` file so you can check later on what the settings were.

The channel Subcommand
----------------------

This is the main purpose for the ``broadcom`` as it was created so someone could change the channel in between running tests. To make it behave like the :ref:`atheros channel changer <atheros-cli>` it does several things:

    #. Set the channel requested

    #. Enable the interface for the channel requested (e.g. if 6 is requested, enable 2.4 GHz)

    #. Disable the other interface (e.g. if 6 is requested, disable 5 GHz)

    #. If the channel is a 5 GHz channel, set the sideband to 'Lower' (the 'Upper' channels are not available)

The command does not output anything to the screen by default and because the command affects both interfaces it is affected by the sleep setting (it has to make a call to the server for each interface and will need to wait in-between to prevent the socket timeout metioned earlier) so if you sit and watch it might seem like it has hung, but it might just be a little slow.

The ``broadcom channel --help``:


.. code::

    usage: broadcom channel [-h] [--undo] [channel]
    
    positional arguments:
      channel     Channel to set (none to get current channels)
    
    optional arguments:
      -h, --help  show this help message and exit
      --undo      Undo the last channel change.
    
    



To set a channel (say channel 36) you use the syntax::

    broadcom channel 36

I also added an ``--undo`` option in case you just want to flip back and forth between two channels. This does *not* change the interface state, though (since I expose enabling and disabling as independent sub-commands), just the channel so it will really only work on one band (I might fix that if this gets extended to another AP).

If you call it without passing in any arguments it will return the current channel setting::

    broadcom channel

The output for this is just a subset of ``status``.

disable and enable
------------------

As I mentioned before, setting the channel enables the interface for the channel chosen and disables the other interface. If you want to enable or disable interfaces independent of this you can use the ``enable`` and ``disable`` subcommands. They operate the same way -- specify a band to apply the sub-command to or leave it blank to apply it to both interfaces::

    broadcom enable 2.4
    broadcom disable 5
    broadcom enable
    broadcom disable

.. note:: These sub-commands don't assume that you only want the specified interface-states (e.g. if you enable 5 GHz it won't automatically disable 2.4 GHz).


.. code::

    usage: broadcom enable [-h] [band]
    
    positional arguments:
      band        Band of interface to enable (2.4, 5 or both) default=both.
    
    optional arguments:
      -h, --help  show this help message and exit
    
    


    
ssid
----

This is a querier to get the SSID. Once again, ``status`` has the SSID in it, so the utility is doubtful, but it is a holding place in case an SSID-setter is implemented later.
