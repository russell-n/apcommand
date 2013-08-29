The ReadOutput
==============
.. currentmodule:: apcommand.commons.readoutput
The `ReadOutput` acts as a file-like object for output.



StandardOutput
--------------

A class to act as a read-only file.

.. autosummary::
   :toctree: api

   StandardOutput

.. uml::

   StandardOutput -|> BaseClass
   StandardOutput : __iter__()
   StandardOutput : readline()
   StandardOutput : readlines()
   StandardOutput : read()



ValidatingOutput
----------------

The ValidatingOutput takes a function ('validate') that is used to check the lines of output as they are read.

.. autosummary::
   :toctree: api

   ValidatingOutput

.. uml::

   ValidatingOutput -|> BaseClass
   ValidatingOutput : __iter__()
   ValidatingOutput : readline()
   ValidatingOutput : readlines()
   ValidatingOutput : read()

