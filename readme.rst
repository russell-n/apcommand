APCommand
=========



This is a command-line controller for an access point (only the Atheros AR5KAP and Broadcom BCM94718NR right now). It was built specifically to allow H. Wong to write some `perl <http://www.perl.org/>`_ code to control the APs. The documentation is online `here <https://bitbucket.org/rallion/apcontrol>`_.

Installation
------------

To install the code change into the top folder and enter::

   python setup.py install

You may need to run this as root if you are installing it system-wide.

The Interface
-------------

Atheros
~~~~~~~

You will end up with a command line command called `atheros` (you can rename it to whatever you find easier to remember). To see the options::

   atheros -h


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
    
    



The `atheros` interface is built around sub-commands (which are listed by the `-h` option). Each sub-command has its own set of options separate from the `atheros`. To see them pass the `-h` option to the sub-command. e.g. to see the `channel` sub-command options::

   atheros channel -h

To actually change the channel to, say 36:

   atheros channel 36

If you aren't familiar with python's sub-command interface note that the options have to go with their sub-command. The `atheros` has a `-d` flag that will output the access points output to the screen (`d` is for `debug`), but the `channel` subcommand doesn't. This is valid::

   atheros -d channel 36

This is not::

   atheros channel 36 -d

.. '

Broadcom
~~~~~~~~

There is also a separate command for the `Broadcom` AP. The interface is similar to the `atheros` command::

   Broadcom -h


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
    
    



.. The Repository
.. --------------
.. 
.. If you did not pull this from bitbucket (or have forgotten where you got it from), the repository is at:
.. 
..    * ssh://hg@bitbucket.org/rallion/apcontrol

The code was written using `pweave <http://mpastell.com/pweave/>`_ so for each ``.py`` file there are accompanying ``.rst`` and ``.pnw`` files.

The Requirements
----------------

When you run the ``install`` command, it will attempt to download `pudb <https://pypi.python.org/pypi/pudb>`_, `requests <https://pypi.python.org/pypi/requests>`_ and `beautifulsoup4 <https://pypi.python.org/pypi/beautifulsoup4>`_. You can get away with removing the `pudb` requirement from the ``conf.py`` file if you don't want to debug the code but `requests` and `beatifulsoup4` are required for it to work.

.. '

The Documentation
-----------------

Since the code was written with `pweave`, the repository is really a sphinx-repository as well as a code repository. To build it you need to have `sphinx` and `sphinxcontrib-plantuml` installed (as well as the code itself). If you don't already have `plantuml <http://plantuml.sourceforge.net/>`_ and you are using a debian-based system you can install it with apt-get::

   apt-get install plantuml

If you don't want to install it, edit the `conf.py` file so it isn't one of the listed extensions and you can still build the documentation, it just won't have any UML diagrams. If have everything installed and you are in the same folder as the ``Makefile`` and ``setup.py`` files then you can type the following to install the requirements and build the documentation (either with admin privileges (i.e. sudo) or in a virtual environment)::

   python setup.py install
   pip install sphinx
   pip install sphinxcontrib-plantuml
   make html

.. '
   
And the documentation will be in a folder called `doc` in the same directory. You can also create a pdf with `make latexpdf` but the code hasn't been groomed for it so it might not look quite right.
   

