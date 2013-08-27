MAIN_HELP_START

::

   usage: apcommand [-h] [--pudb] [--pdb] [-s] [-d] [--hostname HOSTNAME]
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

   usage: apcommand [-h] [--pudb] [--pdb] [-s] [-d] [--hostname HOSTNAME]
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
