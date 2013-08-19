
#python standard library
import argparse


class Arguments(object):
    """
    An adapter for the argparse.ArgumentParser
    """
    def __init__(self):
        self._parser = None
        self._arguments = None
        self._subparsers = None
        return

    @property
    def parser(self):
        """
        :return: ArgumentParser 
        """
        if self._parser is None:
            self._parser = argparse.ArgumentParser()
        return self._parser

    @property
    def arguments(self):
        """
        :return: the parsed command-line arguments
        """
        if self._arguments is None:
            self.add_argument()
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
        self.parser.add_argument("--pudb",
                                 help="Run the `pudb` debugger (default=%(default)s).",
                                 default=False)
        self.parser.add_argument("--pdb",
                                 help="Run the `pdb` debugger (default=%(default)s).",
                                 default=False)
        return

    def add_subparsers(self):
        """
        Add the subparsers to the parser
        """
        up = self.subparsers.add_parser('up', help="Bring the AP up")
        up.set_defaults(function=self.strategy.up)
        return
# end class Arguments
