The Telnet Connection
=====================

.. currentmodule:: apcommand.connections.telnetconnection


The `TelnetConnection` takes the command-line command as a property and the arguments to the command as parameters.

For Example::

    sc = TelnetConnection(hostname='192.168.10.1', username='bob')
    output = sc.ls('-l')
    for line in output.output:
        print line

Prints the output of the `ls -l` command line command.







OutputFile
----------

This acts as a file-like object that traps socket timeouts so that users do not have to know that it contains a networked connection. To prevent blocking the socket-timeout causes it to return a SPACE. 

.. note:: This is also defined in the sshconnection module, but since I wanted to allow for the case where SSH is not used it is re-defined here (otherwise you have to install paramiko)

.. autosummary::
   :toctree: api

   OutputFile

.. uml::

   OutputFile -|> ValidatingOutput
   OutputFile : readline(timeout)




.. _telnet-adapter:

The Telnet Adapter
------------------

The `TelnetAdapter` adapts the built-in python `telnetlib <http://docs.python.org/2/library/telnetlib.html>`_ to make it easier for the :ref:`TelnetConnection <telnet-connection>` to used

.. autosummary::
   :toctree: api

   TelnetAdapter

.. uml::

   TelnetAdapter -|> BaseClass
   TelnetAdapter o-- telnetlib.Telnet
   TelnetAdapter : client
   TelnetAdapter : exec_command(command, timeout)
   TelnetAdapter : writeline(message)







.. _telnet-output:

TelnetOutput
------------

The `TelnetOutput` adapts the :ref:`TelnetAdapter <telnet-adapter>` output to appear more file-like.

.. autosummary::
   :toctree: api

   TelnetOutput

.. uml::

   TelnetOutput -|> BaseClass
   TelnetOutput : readline(timeout)
   TelnetOutput : readlines()
   TelnetOutput : read()
   TelnetOutput : __iter__()




.. _telnet-connection:

The TelnetConnection Class
--------------------------

.. autosummary::
   :toctree: api

   TelnetConnection

.. uml::

   TelnetConnection -|> NonLocalConnection
   NonLocalConnection -|> BaseClass
   BaseClass : logger
   NonLocalConnection : hostname
   NonLocalConnection : username
   NonLocalConnection : password
   NonLocalConnection : command_prefix
   NonLocalConnection : operating_system
   NonLocalConnection: path
   NonLocalConnection : library_path
   NonLocalConnection : lock
   NonLocalConnection o-- threading.RLock
   NonLocalConnection : __getattr__(command)
   NonLocalConnection : __call__(command, arguments)


* The TelnetConnection subclasses :ref:`NonLocalConnection <non-local-connection>` to be compatible with the :ref:`SSHConnection <ssh-connection>`.   

.. note:: The TelnetConnection should be the main interface for both Telnet Servers and Serial-connections. To convert a serial connection to a Telnet connection see  the `pyserial <http://pyserial.sourceforge.net/examples.html#multi-port-tcp-ip-serial-bridge-rfc-2217>`_ tcp-ip serial bridge.
   



.. _telnet-connection-builder:

The TelnetConnectionBuilder
---------------------------

.. autosummary::
   :toctree: api

   TelnetConnectionBuilder

.. uml::

   TelnetConnectionBuilder -|> NonLocalConnectionBuilder

* The TelnetConnectionBuilder is a plugin and so sub-classes the :ref:`NonLocalConnectionBuilder <non-local-connection-builder>`.




Testing the TelnetConnectionBuilder
-----------------------------------

.. autosummary::
   :toctree: api

   TestTelnetConnectionBuilder










