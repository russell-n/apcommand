MAIN_HELP_START

::

   usage: atheros [-h] [--pudb] [--pdb] [-s] [-d] [--hostname HOSTNAME]
                  [--username USERNAME] [--password PASSWORD]
                  {up,down,destroy,status,reset,channel,ssid,security,command}
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
   
     {up,down,destroy,status,reset,channel,ssid,security,command}
                           APCommand sub-commands
       up                  Bring the AP up
       down                Take the AP down
       destroy             Destroy a specific virtual AP
       status              Get some information for an interface
       reset               Reset to factory defaults
       channel             Change the AP channel
       ssid                Change the SSID
       security            Change the security
       command             Execute an arbitrary command.
MAIN_HELP_END
APCOMMAND_OPTIONS_START

::

   usage: atheros [-h] [--pudb] [--pdb] [-s] [-d] [--hostname HOSTNAME]
                  [--username USERNAME] [--password PASSWORD]
                  {up,down,destroy,status,reset,channel,ssid,security,command}
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
APCOMMAND_OPTIONS_END
SUBCOMMAND_HELP_START

::

   APCommand subcommands:
     Available Sub-Commands
   
     {up,down,destroy,status,reset,channel,ssid,security,command}
                           APCommand sub-commands
       up                  Bring the AP up
       down                Take the AP down
       destroy             Destroy a specific virtual AP
       status              Get some information for an interface
       reset               Reset to factory defaults
       channel             Change the AP channel
       ssid                Change the SSID
       security            Change the security
       command             Execute an arbitrary command.

SUBCOMMAND_HELP_END
DESTROY_HELP_START

::

   usage: atheros destroy [-h] interface
   
   positional arguments:
     interface   The VAP name (e.g. ath0)
DESTROY_HELP_END
STATUS_HELP_START

::

   usage: atheros status [-h] [interface]
   
   positional arguments:
     interface   the name of the interface to query (default=ath0) (use 'all' for
                 all)
STATUS_HELP_END
RESET_HELP_START

:: 

   usage: atheros reset [-h] [band]
   
   positional arguments:
     band        2.4 or 5 (default=2.4)
   
   optional arguments:
     -h, --help  show this help message and exit
RESET_HELP_END
CHANNEL_HELP_START

::

   usage: atheros channel [-h] [--mode MODE] [--bandwidth BANDWIDTH] channel
   
   positional arguments:
     channel               Channel to set
   
   optional arguments:
     -h, --help            show this help message and exit
     --mode MODE           Mode (e.g. 11NG)
     --bandwidth BANDWIDTH 
                           Bandwidth (e.g. HT40PLUS)
CHANNEL_HELP_END
SSID_HELP_START

::

   usage: atheros ssid [-h] ssid [band]
   
   positional arguments:
     ssid        The SSID to use
     band        2.4 or 5 (default=2.4)

SSID_HELP_END
