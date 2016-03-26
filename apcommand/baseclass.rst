BaseClass
=========

This is a module to hold base-classes for others to sub-class. 

API
---

.. currentmodule:: apcommand.baseclass

.. autosummary::
   :toctree: api

   BaseClass
   BaseThreadClass







.. base-class::

Class BaseClass
---------------

This is the primary base-class. Sub-classes inherit a `logger` attribute so that they can send operational logging messages to a file.

.. uml::

   BaseClass : logger
   BaseClass o-- logging.Logger




BaseThreadClass
---------------

This is an extension to the `BaseClass` that adds a `run_thread` method that logs tracebacks in the event that an exception is raised. Classes that sub-class it need to implement a `run` method for the `run_thread` method to call and a method to put run_thread into a thread.

.. uml::

   BaseThreadClass <|- BaseClass
   BaseThreadClass : run_thread()
   BaseThreadClass : run()
   BaseThreadClass o-- traceback

* `run` is an abstract method that will raise a NotImplementedError exception if called
   


