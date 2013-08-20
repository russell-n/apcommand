
# this package
from apcommand.baseclass import BaseClass
from apcommand.connections.telnetconnection import TelnetConnection
from apcommand.commons.errors import CommandError


class AtherosAR5KAP(BaseClass):
    """
    A controller for the Atheros AR5KAP
    """
    def __init__(self, hostname='10.10.10.21', username='root', password='5up'):
        """
        The AtherosAR5KAP constructor

        :param:

         - `hostname`: the hostname (IP address) of the AP's telnet interface
         - `username`: the user-login to the AP command-line interface
         - `password`: the password for the AP command-line interface
        """
        super(AtherosAR5KAP, self).__init__()
        self.hostname = hostname
        self.username = username
        self.password = password
        self._connection = None
        return

    @property
    def connection(self):
        """
        The telnet connection to the AP

        :return: TelnetConnection
        """
        if self._connection is None:
            self._connection = TelnetConnection(hostname=self.hostname,
                                                username=self.username,
                                                password=self.password)
        return self._connection

    def log_lines(self, output, error_substring=None):
        """
        Send lines from output to debug log

        :param:

         - `output`: iterable collection of strings
         - `error_substring`: string that raises CommandError if matches

        :postcondition: lines from output sent to debug logger
        :raises: CommandError if error_substring found in output
        """
        for line in output:
            line = line.rstrip()
            if len(line):
                if error_substring is not None and error_substring in line:
                    raise CommandError(line)
                self.logger.debug(line)
        return
        
    def up(self):
        """
        Brings the AP up

        :postcondition: `apup` called on the connection
        """
        output, error = self.connection.apup()
        self.log_lines(output)
        return

    def down(self):
        """
        Takes the AP down

        :postcondition: `apdown` called on the connection
        """
        output, error = self.connection.apdown()
        self.log_lines(output)
        return

    def destroy(self, interface):
        """
        Takes down a VAP

        :param:

         - `interface`: name of VAP

        :postcondition: wlanconfig destroy called on connection
        """
        output, error = self.connection.wlanconfig("{0} destroy".format(interface))
        self.log_lines(output, error_substring='No such device')
        return


# python standard library
import unittest
# third party
from mock import MagicMock


class TestAR5KAP(unittest.TestCase):
    def setUp(self):
        self.logger = MagicMock()
        self.connection = MagicMock()
        self.ap = AtherosAR5KAP()
        self.ap._connection = self.connection
        self.ap._logger = self.logger
        return

    def test_constructor(self):
        """
        Does the constructor set the correct defaults?
        """
        self.assertEqual("10.10.10.21", self.ap.hostname)
        self.assertEqual('root', self.ap.username)
        self.assertEqual('5up', self.ap.password)
        return

    def test_up(self):
        """
        Does the AP controller bring the ap up correctly?
        """
        self.connection.apup.return_value = ('', '')
        self.ap.up()
        self.connection.apup.assert_called_with()
        return

    def test_down(self):
        """
        Does the AP controller bring the AP down?
        """
        self.connection.apdown.return_value = ('', '')
        self.ap.down()
        self.connection.apdown.assert_called_with()
        return

    def test_destroy(self):
        """
        Does the controller bring the VAP down?
        """
        self.connection.wlanconfig.return_value = ('', '')
        self.ap.destroy('ath0')
        self.connection.wlanconfig.assert_called_with("ath0 destroy")

        # vap not up
        self.connection.wlanconfig.return_value = (['wlanconfig: ioctl: No such device\n'], '')
        self.assertRaises(CommandError, self.ap.destroy, ['ath0'])
        return
        

