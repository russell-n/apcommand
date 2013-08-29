The Errors
==========

In order to allow the separation of external errors (those which are not caused by the operation of the code itself) a set of unique errors are used so that the `TestOperation` and `Hortator` can choose what to catch and what to trickle up. Anything not included here is assumed to be an un-recoverable error and should trigger the `CrashHandler`.

.. uml::

   OperatorError -|> Exception
   ComponentError -|> Exception

.. currentmodule:: apcommand.commons.errors

The OperatorError
-----------------

The OperatorError is the base-class for any error that will kill the Test Operation but can be caught by the Hortator to move on to the next Test Operator (if there is one). It is fatal to a test, but not to all testing.

.. autosummary::
   :toctree: api

   OperatorError



The ComponentError
------------------

The ComponentError is the base-class for any error that will kill a particular test-run but allows testing to be continued. It will be caught by the TestOperator and the next repetition will continue. 

.. autosummary::
   :toctree: api
   
   ComponentError



Remote-Connection Errors
------------------------

The Remote-Connection errors are raised if there is a problem communicating with a remote device.

.. currentmodule:: apcommand.commons.errors

.. autosummary::
   :toctree: api

   ConnectionError
   ConnectionWarning
   TimeoutError

.. uml::
   
   OperatorError <|- ConnectionError
   OperatorError <|- ConnectionWarning
   ComponentError <|- TimeoutError

The ConnectionWarning is not used and should be removed.



Command Errors
--------------

A command error is raised if there was an error executing a command. It does not reflect a problem with the system but is specific to the command that was issued on a device.

.. currentmodule:: apcommand.commons.errors

.. autosummary::
   :toctree: api

   CommandError

.. uml::

   CommandError -|> ComponentError
   


StorageError
------------

.. currentmodule:: apcommand.commons.errors

.. autosummary::
   :toctree: api

   StorageError

.. uml::

   StorageError -|> OperatorError
   
A StorageError is raised if there is a problem sending output to the data-storage. This might also be a Configuration Error, depending on what the cause of the error is, but generally it should be the case that there is something wrong with the system that was not caused by user error.




Affector Errors
---------------

Affectors are things that affect the state of the hardware infrastructure (e.g. networked power-switches). These are generally harder to anticipate since we are reaching outside the system.

.. currentmodule:: apcommand.commons.errors

.. autosummary::
   :toctree: api

   AffectorError

.. uml::

   AffectorError -|> ComponentError



User Errors
-----------

These errors are meant for misconfigured configurations or invalid command-line arguments.

.. currentmodule:: apcommand.commons.errors

.. autosummary::
   :toctree: api

   ConfigurationError
   ArgumentError

.. uml::

   OperatorError <|- ConfigurationError
   OperatorError <|- ArgumentError 

