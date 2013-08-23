
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
        output, error = self.connection._main(command)
        
        for line in output:
            print line            
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


NEWLINE = '\n'


class TestArbitraryCommand(unittest.TestCase):
    """
    Test The ArbitraryCommand
    """
    def setUp(self):
        self.connection = MagicMock()
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

        self.connection._main.return_value = (output, error)
        stdout = MagicMock()
        with patch('sys.stdout', stdout):
            self.command(command)
        self.connection._main.assert_called_with(command)

        calls =  stdout.mock_calls
        expected = [call.write(output[0]), call.write(NEWLINE)]
        self.assertEqual(expected, calls)
        self.logger.debug.assert_called_with(output[0])
        self.logger.error.assert_called_with(error[0])
        return
