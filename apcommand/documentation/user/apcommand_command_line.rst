The `apcommand`
===============

After installing this package::

   python setup.py install

you will end up with a command-line command called `apcommand`. If you inspect it you'll see that it's just a text file that calls the entry-point to this code (defined in the `setup.py` file). If that doesn't mean anything to you, don't worry, I bring it up to point out that it's nothing special so you can rename it if you want (or move it anywhere on your PATH).

The Command-Line Interface
--------------------------

The command-line interface is built using python's `argparse <http://docs.python.org/2/library/argparse.html>`_. To get a listing of the available options you use the ``-h`` or ``--help`` options::

   apcommand --help

You should see something like:

.. include:: help_output.rst
   :start-after: MAIN_HELP_START
   :end-before: MAIN_HELP_END

.. warning:: I'm still working on the code so it might not look exactly like this.

I'll explain the sub-commands in the next section so for now just look at the top sections (`usage` and `optional arguments`).

The Usage Help
~~~~~~~~~~~~~~

.. include:: help_output.rst
   :start-after: APCOMMAND_OPTIONS_START
   :end-before: APCOMMAND_OPTIONS_END

The `usage` line is telling you what you would type at the command line to use the `apcommand`. Anything in square brackets ([]) is optional and is given more detail under the `optional arguments` section. The things in curly braces ({}) are sub-commands (see below). The `hostname`, `username`, and `password` are set for the Atheros AR5KAP:

.. csv-table:: Atheros Telnet Defaults
   :header: Option, Value

   hostname,10.10.10.21
   username,root
   password,5up

You shouldn't have to change them but if you do need to pass them in *before* the subcommand::

   apcommand --hostname 192.168.10.65 <subcommand>

Where <subcommand> is one of those listed in the curly-braces.

The only other option you might want to use is ``--debug`` (or equivalently ``-d``). This will send the output from the AP's command line to standard out -- by default it is being saved to a log file but since it's so noisy it isn't emitted unless you ask for it. The first few times you run it you might want to use this option, as it takes a while to actually change the AP's settings (or you can just tail the log -- ``tail -f apcommand.log``).


The Sub-Commands
----------------

A mentioned above the `apcommand` interface is built around argparse and in particular uses the `sub-command <http://docs.python.org/2/library/argparse.html#sub-commands>`_ feature. The current sub-commands are:

.. include:: help_output.rst
   :start-after: SUBCOMMAND_HELP_START
   :end-before: SUBCOMMAND_HELP_END

up and down
~~~~~~~~~~~

The `up` and `down` subcommands execute the :ref:`apup <apup-code>` and :ref:`apdown <apdown-code>` commands on the AP. 

So::

   apcommand up

Is the equivalent of logging on to the AP and typing::

   apup

destroy
~~~~~~~

The `destroy` subcommand takes down a VAP that you pass it. It uses `wlanconfig` so it only works on Virtual AP's. I added it because I accidentally turned on both the 5 GHz and 2.4 GHz bands at the same time and needed to destroy the extra VAP (*ath1*) that was created. 

Doing this::

   apcommand destroy ath1

Is the equivalent of logging on to the AP and typing::

   wlanconfig ath1 destroy



