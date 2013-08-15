The SSHConnection
=================

Contents:

   * :ref:`SSHClient <ssh-client>`

   * :ref:`SimpleClient <simple-client>`

   * :ref:`SSHConnection <ssh-connection>`

   * :ref:`OutputFile <output-file>`

   * :ref:`SSHConnectionBuilder <ssh-connection-builder>`

Encapsulates the Paramiko `SSHClient <http://www.lag.net/paramiko/docs/paramiko.SSHClient-class.html>`_ to provide a common interface with the other connection types.

.. currentmodule:: apcommand.connections.sshconnection
   


.. _ssh-client:

SSHClient
---------

This is an extension of paramiko.SSHClient that adds a timeout to the output read attempts. It can be used transparently the same way the paramiko SSHClient is used or with the added ``timeout`` parameter.

.. autosummary::
   :toctree: api
   
   SSHClient

.. uml::

   SSHClient -|> paramiko.SSHClient
   SSHClient : exec_command(command, timeout, bufsize, combine_stderr)
   SSHClient : invoke_shell(term, width, Height, timeout, bufsize)
   SSHClient : invoke_shell_rw(term, width, Height, timeout, bufsize)
   


.. _simple-client:

SimpleClient
------------

This is a wrapper around the :ref:`SSHClient <ssh-client>` that sets some flags to avoid host-key errors. The following are (roughly) equivalent.

SSHClient::

   c = SSHClient()
   c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   c.load_system_host_keys()
   c.connect(hostname='192.168.10.24', username='tester')
   stdin, stdout, stderror = c.exec_command('ls')

SimpleClient::

   c = SimpleClient(hostname='192.168.10.24', username='tester')
   stdin, stdout, stderr = c.exec_command('ls')
   
.. autosummary::
   :toctree: api

   SimpleClient

.. uml::

   SimpleClient -|> BaseClass
   SimpleClient o-- SSHClient
   SimpleClient : client
   SimpleClient : hostname
   SimpleClient : username
   SimpleClient : password
   SimpleClient : port
   SimpleClient : timeout
   SimpleClient : exec_command(command, timeout)
   SimpleClient : __str__()
   SimpleClient : close()




.. _ssh-connection:

The SSHConnection
-----------------

This class uses the :ref:`SimpleClient <simple-client>` to implement the :ref:`NonLocalConnection <non-local-connection>` interface.

.. autosummary::
   :toctree: api

   SSHConnection

.. uml::

   SSHConnection -|> NonLocalConnection
   NonLocalConnection : logger
   NonLocalConnection : __getattr__(command, arguments, timeout)
   NonLocalConnection : __call__(command, arguments, timeout)   
   SSHConnection o-- SimpleClient
   SSHClient : client
   SSHConnection : hostname
   SSHConnection : username
   SSHConnection : password
   SSHConnection : port
   SSHConnection : timeout

To see the difference between the :ref:`SimpleClient <simple-client>` and the `SSHConnection` I will compare the same command executed on both of them.

SimpleClient Example::

   connection = SimpleClient(hostname='192.168.10.24', username='tester')
   stdin, output, error = connection.exec_command('ls -l')
   for line in output:
       print line

   for line in error:
       print line
   
Equivalent SSHConnection Example::
         
    connection = SSHConnection(username="tester", hostname="192.168.10.24")
    output, error = connection.ls('-l')
    for line in output:
        print line

    for line in error:
        print line




.. _output-file:

OutputFile
----------

This acts as a file-like object that traps socket timeouts so that users do not have to know that it contains a networked connection. To prevent blocking the socket-timeout causes it to return a SPACE. 

.. autosummary::
   :toctree: api

   OutputFile

.. uml::

   OutputFile -|> ValidatingOutput
   OutputFile : readline(timeout)



Another Example
---------------

..
    if __name__ == "__main__":
        c = SSHConnection('igor', 'developer')
        o = c.wmic('path win32_networkadapter where netconnectionid="\'Wireless Network Connection\'" call enable')
        for index, line in enumerate(o.output):
            print index, line

.. _ssh-connection-builder:
            
The SSHConnectionBuilder
------------------------

In order to create a uniform plugin interface, each connection is required to implement the `NonLocalConnectionBuilder` interface (because the current assumption is that the :ref:`Serial <serial-connection>` will be translated to a :ref:`Telnet <telnet-connection>` and the :ref:`Local <local-connection>` will be translated to a :ref:`SSH Connection <ssh-connection>`).

.. autosummary::
   :toctree: api

   SSHConnectionBuilder

.. uml::

   SSHConnectionBuilder -|> NonLocalConnectionBuilder
   NonLocalConnectionBuilder : parameters
   NonLocalConnectionBuilder : product

Example Use::

   builder = SSHConnectionBuilder()
   builder.parameters = parameters
   Connection = builder.product

Note that this is a plugin so the example is a bit of a fake. The real way to get it would be::

    plugin_manager = PluginManagerSingleton.get()
    plugin_manager.setPluginPlaces(arachne.PLUGIN_PLACES)
    plugin_manager.setPluginInfoExtension(arachne.PLUGIN_EXTENSION)
    plugin_manager.setCategoriesFilter({arachne.CONNECTION_CATEGORY:NonLocalConnectionBuilder})
    plugin_manager.collectPlugins()
    builder = plugin_manager.getPluginByName(sshconnection.PLUGIN_NAME,
                                             arachne.CONNECTION_CATEGORY)

    parameters = nonlocalconnection.ConnectionParameters(hostname='elin',
                                                         username='tester',
                                                         password=None,
                                                         operating_system='linux',
                                                         path=None,
                                                         library_path=None,
                                                         port=5286)

    builder.parameters = parameters
    connection = builder.product
    




Testing the SSHConnectionBuilder
--------------------------------

.. autosummary::
   :toctree: api

   TestSSHConnectionBuilder.test_plugin
   TestSSHConnectionBuilder.test_product
   TestSSHConnectionBuilder.test_defaults





