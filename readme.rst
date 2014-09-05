APCommand
=========

This is a command-line controller for an access point (only the Atheros AR5KAP right now). It was built specifically to allow H. Wong to write some `perl <http://www.perl.org/>`_ code to marry with Aren's code to allow changing channels in between test-runs. See the online documentation `here <http://rallion.bitbucket.org/commands/ap_command/index.html>`_.

The Interface
-------------

Once you install the code::

   python setup.py install

You will end up with a command line command called `atheros` (you can rename it to whatever you find easier to remember). To see the options::

   atheros -h

The `atheros` interface is built around sub-commands (which are listed by the `-h` option). Each sub-command has its own set of options separate from the `atheros`. To see them pass the `-h` option to the sub-command. e.g. to see the `channel` sub-command options::

   atheros channel -h

To actually change the channel to, say 36:

   atheros channel 36

If you aren't familiar with python's sub-command interface note that the options have to go with their sub-command. The `atheros` has a `-d` flag that will output the access points output to the screen (`d` is for `debug`), but the `channel` subcommand doesn't. This is valid::

   atheros -d channel 36

This is not::

   atheros channel 36 -d


The Repository
--------------

If you did not pull this from bitbucket (or have forgotten where you got it from), the repository is at:

   * ssh://hg@bitbucket.org/rallion/apcontrol

The code was written using `pweave <http://mpastell.com/pweave/>`_ so for each ``.py`` file there are accompanying ``.rst`` and ``.pnw`` files.

The Requirements
----------------

Since I currently only support telnet there should be no extra requirements. I dumped what's currently installed in my virtual environment (python packages only) into the `requirements.txt` file. Most of the things in there are for testing, debugging, pweave, and sphinx. Unless you plan to do any of those things you shouldn't need to install anything. That being said, to understand how to use this you should probably read the documentation, which actually does require you to install things (See the next section).

The Documentation
-----------------

Since the code was written with pweave, the repository is really a sphinx-repository as well as a code repository. To build it you need to have `sphinx` and `sphinxcontrib-plantuml` installed (as well as the code itself). If you are in the same folder as the ``Makefile`` and ``setup.py`` files then you can type the following to install the requirements and build the documentation (either with admin privileges (i.e. sudo) or in a virtual environment)::

   python setup.py install
   pip install sphinx
   pip install sphinxcontrib-plantuml
   make html

And the documentation will be in a folder called `build` in the same directory. You can also create a pdf with `make latexpdf` but the code hasn't been groomed for it so it might not look quite right.
   

