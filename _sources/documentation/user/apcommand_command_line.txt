The `atheros` Command
=====================



After installing this package::

   python setup.py install

you will end up with a command-line command called `atheros`. If you inspect it you'll see that it's just a text file that calls the entry-point to this code (defined in the `setup.py` file). If that doesn't mean anything to you, don't worry, I bring it up to point out that it's nothing special so you can rename it if you want (or move it anywhere on your PATH).

.. _atheros-cli:

The Command-Line Interface
--------------------------


The command-line interface is built using python's `argparse <http://docs.python.org/2/library/argparse.html>`_. To get a listing of the available options you use the ``-h`` or ``--help`` options::

   atheros --help

You should see something like:

.. .. include:: help_output.rst
..    :start-after: MAIN_HELP_START
..    :end-before: MAIN_HELP_END


.. code::

    usage: atheros [-h] [--pudb] [--pdb] [-s] [-d] [--hostname HOSTNAME]
                   [--username USERNAME] [--password PASSWORD]
                   {up,down,destroy,status,reset,channel,ssid,ip,security,command}
                   ...
    
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
    
    APCommand subcommands:
      Available Sub-Commands
    
      {up,down,destroy,status,reset,channel,ssid,ip,security,command}
                            APCommand sub-commands
        up                  Bring the AP up
        down                Take the AP down
        destroy             Destroy a specific virtual AP
        status              Get some information for an interface
        reset               Reset to factory defaults
        channel             Change the AP channel
        ssid                Change the SSID
        ip                  Change the IP Address
        security            Change the security
        command             Execute an arbitrary command.
    
    




I'll explain the sub-commands in the next section so for now just look at the top sections (`usage` and `optional arguments`).

.. '

The Usage Help
~~~~~~~~~~~~~~

.. literalinclude:: help_output.rst
   :start-after: APCOMMAND_OPTIONS_START
   :end-before: APCOMMAND_OPTIONS_END

The `usage` line is telling you what you would type at the command line to use the `atheros`. Anything in square brackets ([]) is optional and is given more detail under the `optional arguments` section. The things in curly braces ({}) are sub-commands (see below). The `hostname`, `username`, and `password` for the Atheros AR5KAP are set as defaults:

.. csv-table:: Atheros Telnet Defaults
   :header: Option, Value

   hostname,10.10.10.21
   username,root
   password,5up

You shouldn't have to change them but if you do pass them in *before* the subcommand. For example, to change the *hostname* for the AP and get its status::

   atheros --hostname 192.168.10.65 status


The only other option you might want to use is ``--debug`` (or equivalently ``-d``). This will send the output from the AP's command line to standard out -- by default it is being saved to a log file but since it's so noisy it isn't emitted unless you ask for it. The first few times you run it you might want to use this option, as it takes a while to actually change the AP's settings and it might feel as though it's hung up so this will give you some feedback (alternatively, you can tail the log -- ``tail -f atheros.log``).

.. _atheros-subcommands:

The Sub-Commands
----------------

As mentioned above the `atheros` interface is built around `argparse` and in particular uses the `sub-command <http://docs.python.org/2/library/argparse.html#sub-commands>`_ feature. The current sub-commands are:

.. include:: help_output.rst
   :start-after: SUBCOMMAND_HELP_START
   :end-before: SUBCOMMAND_HELP_END

.. _up-and-down-subcommand:

up and down
~~~~~~~~~~~

The `up` and `down` subcommands execute the `apup` and `apdown` commands on the AP. 

So::

   atheros up

Is the equivalent of logging on to the AP and typing::

   apup

.. _destroy-subcommand:

destroy
~~~~~~~

The `destroy` subcommand takes down a VAP that you pass it. It uses `wlanconfig` so it only works on Virtual AP's. I added it because I accidentally turned on both the 5 GHz and 2.4 GHz bands at the same time and needed to destroy the extra VAP (*ath1*) that was created. 

.. '

Doing this::

   atheros destroy ath1

Is the equivalent of logging on to the AP and typing::

   wlanconfig ath1 destroy
   
This is help output for the `destroy` sub-command:

.. .. include:: help_output.rst
..    :start-after: DESTROY_HELP_START
..    :end-before: DESTROY_HELP_END


.. code::

    usage: atheros destroy [-h] interface
    
    positional arguments:
      interface   The VAP name (e.g. ath0)
    
    optional arguments:
      -h, --help  show this help message and exit
    
    



.. _status-subcommand:

status
~~~~~~

This subcommand just dumps the `iwconfig`, `ifconfig` IP address, and the `iwlist` channel settings::

   atheros status

Is the equivalent of logging on to the AP and typing::

   iwconfig ath0
   ifconfig ath0 | grep "inet addr"
   iwlist ath0 channel | grep Current

The `status -h` output:

.. .. include:: help_output.rst
..    :start-after: STATUS_HELP_START
..    :end-before: STATUS_HELP_END


.. code::

    usage: atheros status [-h] [interface]
    
    positional arguments:
      interface   the name of the interface to query (default=ath0) (use 'all' for
                  all interfaces)
    
    optional arguments:
      -h, --help  show this help message and exit
    
    



.. _reset-subcommand:

reset
~~~~~

This tells the AP to erase any configurations that have been made and set it back to the defaults::

   atheros reset

is the equivalent of logging on to the AP and entering::

   apdown
   cfg -x

The `reset -h` output:

.. .. include:: help_output.rst
..    :start-after: RESET_HELP_START
..    :end-before: RESET_HELP_END


.. code::

    usage: atheros reset [-h] [band]
    
    positional arguments:
      band        2.4 or 5 (default=2.4)
    
    optional arguments:
      -h, --help  show this help message and exit
    
    



.. warning:: The `band` argument might be misleading -- you are resetting both bands, but this option specifies which band to bring back up after resetting the AP.

If you want to see the defaults you can inspect the `/etc/ath/apcfg` file.

.. _channel-subcommand:

channel
~~~~~~~

This changes the channel using the default bandwidths chosen::

   atheros channel 1

sets the channel to 1 and the bandwidth to HT20, whereas::

   atheros channel 36

sets the channel to 36 and the bandwidth to HT40+ and::

   atheros channel 40

sets the channel to 40 and the bandwidth to HT40-, and so on.

The `channel -h` output:

.. .. include:: help_output.rst
..    :start-after: CHANNEL_HELP_START
..    :end-before: CHANNEL_HELP_END


.. code::

    usage: atheros channel [-h] [--mode MODE] [--bandwidth BANDWIDTH] channel
    
    positional arguments:
      channel               Channel to set
    
    optional arguments:
      -h, --help            show this help message and exit
      --mode MODE           Mode (e.g. 11NG)
      --bandwidth BANDWIDTH
                            Bandwidth (e.g. HT40PLUS)
    
    



.. _ssid-subcommand:

ssid
~~~~

This sets the broadcast SSID for the AP::

   atheros ssid amanaplanacanalpanama

The ``ssid -h`` output:

.. .. include:: help_output.rst
..    :start-after: SSID_HELP_START
..    :end-before: SSID_HELP_END


.. code::

    usage: atheros ssid [-h] ssid [band]
    
    positional arguments:
      ssid        The SSID to use
      band        2.4 or 5 (default=2.4)
    
    optional arguments:
      -h, --help  show this help message and exit
    
    



.. _security-subcommand:

security
~~~~~~~~

This sets the security for the AP, but hasn't been implemented yet.

.. _command-subcommand:

command
~~~~~~~

This executes an arbitrary command on the AP and sends its output to standard out. This was implemented so that if I forgot anything you can always type it in::

    atheros command dmesg

will dump the current /proc/kmsg file to standard output while::

   atheros command 'ping -c 1 www.google.com'

will send one ping from the AP to google. Note two things:

   * The command string is put in quotes (``'ping -c'`` is seen as one word while ``ping -c`` would be seen as two)

   * The ``ping`` is given the ``-c 1`` -- I didn't implement anything to handle calls that don't end -- this includes ``cat /proc/kmsg`` or similar calls that require ``ctrl-c`` to terminate them. I think that for ping it will run forever while the ``cat /proc/kmsg`` will eventually quit with a socket timeout.

