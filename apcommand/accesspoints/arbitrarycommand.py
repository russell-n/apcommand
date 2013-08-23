
# python standard library
import sys
# this package
from apcommand.baseclass import BaseClass


class ArbitraryCommand(BaseClass):
    """
    An arbitrary command class
    """
    def __init__(self, connection):
        """
        Arbitrary command constructor

        :param:

         - `connection`: connection to send commands to
        """
        self.connection = connection
        super(ArbitraryCommand, self).__init__()
        return

    def __call__(self, command):
        """
        The main interface - sends the command to the connection and outputs output
        """
        output, error = self.connection.exec_command(command)
        
        for line in output:
            sys.stdout.write(line)
            self.logger.debug(line)
        for line in error:
            if len(line):
                self.logger.error(line)
        return
        


# python standard library
import unittest
import random
import string

# third-party
from mock import MagicMock, patch, call

# this package
from apcommand.connections.telnetconnection import TelnetConnection


NEWLINE = '\n'


class TestArbitraryCommand(unittest.TestCase):
    """
    Test The ArbitraryCommand
    """
    def setUp(self):
        self.connection = MagicMock(spec=TelnetConnection)
        self.logger = MagicMock()
        self.command = ArbitraryCommand(connection=self.connection)
        self.command._logger = self.logger
        return

    def test_constructor(self):
        """
        Does the constructor set the connection?
        """
        self.assertEqual(self.connection, self.command.connection)
        self.assertEqual(self.logger, self.command.logger)
        return

    def test_call(self):
        """
        Does the call send the command to the connection?
        """
        command = ''.join([random.choice(string.printable) for i in range(random.randrange(100))])
        output = [''.join([random.choice(string.printable) for i in range(random.randrange(100))])]
        error = [''.join([random.choice(string.printable) for i in range(random.randrange(100))])]

        self.connection.exec_command.return_value = (output, error)
        stdout = MagicMock()
        with patch('sys.stdout', stdout):
            self.command(command)
        self.connection.exec_command.assert_called_with(command)

        stdout.write.assert_called_with(output[0])
        self.logger.debug.assert_called_with(output[0])
        self.logger.error.assert_called_with(error[0])
        return
