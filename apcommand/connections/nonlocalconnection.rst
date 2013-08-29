The Non-Local Connection
========================

The Non-Local Connection is a Base for non-local connectionS (e.g. SSH or Telnet).

Calls to a NonLocalConnection takes the command-line command as a property and the arguments to the command as parameters. For example, if the command is ``ps`` and the argument is ``-e`` then a connection would be called like this::

    output, error = connection.ps('-e')
    for line in output:
        print line

The ``output`` and ``error`` are actually unpacking the :ref:`OutputError <output-error>` namedtuple defined in the `localconnection` module. An alternative way to make the same call would be::

    output_error = connection.ps('-e')
    for line in output_error.output:
        print line

Although the dot-notation is the primary interface, there are cases where the command contains a dot (e.g. `wifi.sh`) which renders it unusable. For those cases you can use the ``__call__`` method instead::

   output, error = connection(command='wifi.sh', arguments='status', timeout=1)

The `__call__` is actually an alias for the `_procedure_call` method, but is provided to to keep the interface more consistent with other classes in the package, and hopefully reduce the likelihood of error caused by having to remember the name of the method (I never can).

.. currentmodule:: apcommand.connections.nonlocalconnection
.. autosummary::
   :toctree: api

   NonLocalConnection

The primary features the `NonLocalConnection` adds to children that inherit from it are the setting of a command prefix (based on the `PATH` and `LD_LIBRARY_PATH` variables) and the dot-notation interface. Additionally, since it inherits from the :ref:`BaseClass <base-class>` all children have a `logger` attribute.



.. _non-local-connection:

The NonLocalConnection
----------------------

.. uml::

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

.. note:: The port is not set in the `NonLocalConnection` so that child-classes can set a default port number for themselves.

.. warning:: Because the ``_getattr__`` is defined, children of this class need to be aware that if a user of the child-class tries to get a property that was not defined in the class they will *not* get an `AttributeError <http://docs.python.org/2/reference/expressions.html#attribute-references>`_ but will instead get the ``__getattr__`` method returned. e.g. if you did not define ``SSHConnection.nickname`` but a user tried to retrieve it -- ``nick = connection.nickname`` -- the ``nick`` variable would now contain a reference to ``connection.__getattr__`` which might not be what was expected.



The NonLocalConnectionBuilder
-----------------------------

.. currentmodule:: apcommand.connections.nonlocalconnection
.. autosummary::
   :toctree: api

   NonLocalConnectionBuilder

.. uml::

   NonLocalConnectionBuilder o-- logging.Logger
   NonLocalConnectionBuilder : parameters
   NonLocalConnectionBuilder : product
   NonLocalConnectionBuilder : _logger
   


ConnectionParameters
-------------

This is a named-tuple to pass parameters to the non-local-connection.

.. autosummary::
   :toctree: api

   ConnectionParameters

.. uml::

   ConnectionParameters -|> collections.namedtuple
   ConnectionParameters : hostname
   ConnectionParameters : username
   ConnectionParameters : password
   ConnectionParameters : operating_system
   ConnectionParameters : path
   ConnectionParameters : library_path
   ConnectionParameters : port
   


Testing the NonLocalConnection
------------------------------

.. autosummary::
   :toctree: api

   TestNonLocalConnection.test_main
   TestNonLocalConnection.test_add_path
   TestNonLocalConnection.test_getattr
   TestNonLocalConnection.test_command_prefix



Testing the NonLocalConnectionBuilder
-------------------------------------

.. autosummary::
   :toctree: api

   TestNonLocalConnectionBuilder.test_product
   TestNonLocalConnectionBuilder.test_attributes







