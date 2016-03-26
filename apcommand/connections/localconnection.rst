The Local Connection
====================
.. currentmodule:: apcommand.connections.localconnection
.. note:: In practice I have found that there is almost no case where you cannot use telnet or ssh to connect to a device, and both have more robust interfaces (as well as allowing remote access), so this is pretty much never used or maintained anymore.

e.g.::

    lc = LocalConnection()
    output = lc.ls('-l')
    print output.output

This will print the output of the ``ls -l`` command line command.

This is using subprocess so anything with lots of output runs the risk of causing the output to block (i.e. it is file-buffered, not line or character buffered).

In most cases it is better to use the LocalNixConnection instead which uses Pexpect to avoid the block.







The OutputError
---------------

This is a namedtuple to contain standard-out and standard-error.

.. uml::

   OutputError -|> collections.namedtuple
   OutputError : output
   OutputError : error




The LocalConnection
-------------------

.. autosummary::
   :toctree: api

   LocalConnection -|> BaseClass
   LocalConnection : command_prefix
   



LocalNixConnection
------------------

This class is like the LocalConnection but does not suffer from the problem if stdout blocking the way the LocalConnection. Because it uses `Pexpect` only unix-like systems can use it.




