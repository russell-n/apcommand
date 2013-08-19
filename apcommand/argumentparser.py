
#python standard library
import argparse

# this packag
import subcommands


class Arguments(object):
    """
    An adapter for the argparse.ArgumentParser
    """
    def __init__(self):
        """
        Arguments Constructor
        """
        self._parser = None
        self._arguments = None
        self._subparsers = None
        self._subcommands = None
        return

    @property
    def subcommands(self):        
        """
        The SubCommands object for the parser sub-commands
        """
        if self._subcommands is None:
            self._subcommands = subcommands.SubCommand()
        return self._subcommands

    @property
    def parser(self):
        """
        The argparse Argument Parser
        
        :return: ArgumentParser 
        """
        if self._parser is None:
            self._parser = argparse.ArgumentParser()
        return self._parser

    @property
    def arguments(self):
        """
        The namespace containing the command-line arguments
        
        :return: the parsed command-line arguments
        """
        if self._arguments is None:
            self.add_arguments()
            self.add_subparsers()
            self._arguments = self.parser.parse_args()
        return self._arguments

    @property
    def subparsers(self):
        """
        The subparsers for the parser

        :return: ArgumentParser subparsers
        """
        if self._subparsers is None:
            self._subparsers = self.parser.add_supparsers(title="APCommand subcommands",
                                                          description="Available Sub-Commands",
                                                          help="APCommand sub-commands")
        return self._subparsers

    def add_arguments(self):
        """
        Add the command-line arguments to the parser
        """
        # debugging
        self.parser.add_argument("--pudb",
                                 action='store_true',
                                 help="Run the `pudb` debugger (default=%(default)s).",
                                 default=False)
        self.parser.add_argument("--pdb",
                                 action='store_true',
                                 help="Run the `pdb` debugger (default=%(default)s).",
                                 default=False)
        # logging
        self.parser.add_argument('-s', '--silent',
                                 action='store_true',
                                 help="If True only emit error messages (default=%(default)s)",
                                 default=False)
        
        self.parser.add_argument('-d', '--debug',
                                 action='store_true',
                                 help='If True emit debug messages (default=%(default)s)',
                                 default=False)
        return

    def add_subparsers(self):
        """
        Add the subparsers to the parser
        """
        up = self.subparsers.add_parser('up', help="Bring the AP up")
        up.set_defaults(function=self.subcommands.up)
        return
# end class Arguments
