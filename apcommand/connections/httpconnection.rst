HTTP Connection
===============
.. currentmodule:: apcommand.connections.httpconnection
This is a client-connection to communicate with HTTP-servers. Since some of the parameters are reminiscent of telnet and SSH sessions I will model it somewhat after the SSHConnection, but it will primarily act as an interface to the `requests <http://docs.python-requests.org/en/latest/>`_ package.

.. uml::

   HTTPConnection o- requests.Request
   HTTPConnection : GET(*args, **kwargs)

.. autosummary::
   :toctree: api

   HTTPConnection

The URL is being put together with the python `urlparse.urlunparse <http://docs.python.org/2/library/urlparse.html>`_ method. For future reference, the tuple that is passed to it has these fields:

.. csv-table:: ParseResult tuple
   :header: Name, Index, Description, Default
   
   scheme, 0, URL scheme specifier, empty string
   netloc, 1, Network location part, empty string
   path, 2, Hierarchical path, empty string
   params, 3, Parameters for last path element, empty string
   query, 4, Query component, empty string
   fragment, 5, Fragment identifier, empty string




