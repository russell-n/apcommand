
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
        self._logger = None
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

    def log_lines(self, output, error_substring=None, level='debug'):
        """
        Send lines from output to debug log

        :param:

         - `output`: iterable collection of strings
         - `error_substring`: string that raises CommandError if matches

        :postcondition: lines from output sent to debug logger
        :raises: CommandError if error_substring found in output
        """
        if level == 'info':
            logger = self.logger.info
        else:
            logger =  self.logger.debug
        for line in output:
            line = line.rstrip()
            if len(line):
                if error_substring is not None and error_substring in line:
                    raise CommandError(line)
                logger(line)
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

    def status(self, interface):
        """
        Check iwconfig and ifconfig for the interface

        :param:

         - `interface`: name of network interface (e.g. ath0)
        """
        output, error = self.connection.iwconfig(interface)
        self.log_lines(output, level='info', error_substring='No such device')
        output, error = self.connection.ifconfig("{0} | grep 'inet addr'".format(interface))
        self.log_lines(output, level='info', error_substring='Device not found')
        output, error = self.connection.iwlist("{0} channel | grep Current".format(interface))
        self.log_lines(output, level='info')
        return

    def reset(self, interface):
        """
        Clears the AP configuration back to the factory defaults

        *the interface just tears down the other interface - both will still be reset*

        :param:

         - `interface`: the name of the VAP (etc. ath0)
        """
        with Configure(connection=self.connection, interface=interface):
            output, error = self.connection.cfg('-x')
        return


class Atheros24(AtherosAR5KAP):
    """
    A channel-changer for 2.4 GHz
    """
    def __init__(self, *args, **kwargs):
        """
        Atheros24 constructor
        """
        super(Atheros24, self).__init__(*args, **kwargs)
        return

    def set_channel(self, channel):
        """
        method to set the channel on the AP

        :param:

         - `channel`: string or integer in {1,..., 11}
        """
        with Configure(connection=self.connection, interface='ath0'):
            output, error = self.connection.cfg('-a AP_CHMODE={0}HT20'.format(channel))
            self.log_lines(output)
            output, error = self.connection.cfg('-a AP_PRIMARY_CH={0}'.format(channel))
            self.log_lines(output)
            output, error = self.connection.cfg('-a AP_RADIO_ID=0')
            self.log_lines(output)
        return
    


# python standard library
import unittest
# third party
from mock import MagicMock, call
from nose.tools import raises


EMPTY_TUPLE = ('','')

class TestAR5KAP(unittest.TestCase):
    def setUp(self):
        self.logger = MagicMock()
        self.connection = MagicMock()
        self.ap = AtherosAR5KAP()
        self.ap._connection = self.connection
        self.ap._logger = self.logger
        self.enter_calls = [call.apdown()]
        self.exit_calls = [call.cfg('-c'), call.apup(),
                           call.wlanconfig("ath1 destroy")]

        return

    def set_context_connection(self):
        self.connection.apdown.return_value = EMPTY_TUPLE
        self.connection.cfg.return_value = EMPTY_TUPLE
        self.connection.apup.return_value = EMPTY_TUPLE
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

    def test_status(self):
        """
        Does the controller query iwconfig and ifconfig?
        """
        self.connection.iwconfig.return_value = ('', '')
        self.connection.ifconfig.return_value = ('', '')
        self.connection.iwlist.return_value = ('','')
        self.ap.status('ath0')
        self.connection.iwconfig.assert_called_with("ath0")
        self.connection.ifconfig.assert_called_with("ath0 | grep 'inet addr'")
        self.connection.iwlist.assert_called_with("ath0 channel | grep Current")

        self.connection.iwconfig.return_value = (['ath0: No such device\n'], '')
        self.assertRaises(CommandError, self.ap.status, ['ath0'])
        return

    def test_ifconfig_fail(self):
        """
        Does a missing interface raise a Command Error?
        """
        self.connection.iwconfig.return_value = ('','')
        self.connection.ifconfig.return_value = (['ifconfig: ath0: error fetching interface information: Device not found\n'], '')
        self.connection.iwlist.return_value = ('','')
        self.assertRaises(CommandError, self.ap.status, ['ath0'])
        return

    def test_reset(self):
        """
        Does the reset clear the configuration?
        """
        self.set_context_connection()
        self.ap.reset(interface='ath0')
        calls = self.enter_calls + [call.cfg('-x')] + self.exit_calls
        self.assertEqual(calls, self.connection.method_calls)
        return


class Configure(BaseClass):
    """
    A context manager for configure commands on the Atheros
    """
    def __init__(self, connection, interface):
        """
        The Configure constructor -- this will destroy the other interface on exit

        :param:

         - `connection`: connection to AP's command-line interface
         - `interface`: the interface (ath0 or ath1)
        """
        super(Configure, self).__init__()
        self.connection = connection
        self.interface = interface
        self._other_interface = None
        self.logger.debug(str(connection))
        self.logger.debug("interface: {0}".format(interface))
        return

    @property
    def other_interface(self):
        """
        The other VAP interface (to be destroyed)

        :return: name of other interface (e.g. ath0 if self.inteface is ath1)
        :raise: CommandError if interface is not ath0 or ath1
        """
        if self.interface == 'ath0':
            return 'ath1'
        elif self.interface == 'ath1':
            return 'ath0'
        raise CommandError("Unknown Interface (VAP): {0}".format(self.interface))
            

    def __enter__(self):
        """
        Takes down the AP
        """
        output, error = self.connection.apdown()
        self.log_lines(output)
        return self.connection

    def __exit__(self, type, value, traceback):
        """
        Commits the configuration and brings up the AP, destroying the other VAP
        """
        empty_tuple = ('','')
        self.connection.cfg.return_value = empty_tuple
        self.connection.apup.return_value = empty_tuple
        self.connection.wlanconfig.return_value = empty_tuple
        
        output, error = self.connection.cfg('-c')
        self.log_lines(output)
        output, error = self.connection.apup()
        self.log_lines(output)
        output, error = self.connection.wlanconfig('{0} destroy'.format(self.other_interface))
        self.log_lines(output)
        return
    
    def log_lines(self, output, error_substring=None, level='debug'):
        """
        Send lines from output to debug log

        :param:

         - `output`: iterable collection of strings
         - `error_substring`: string that raises CommandError if matches

        :postcondition: lines from output sent to debug logger
        :raises: CommandError if error_substring found in output
        """
        if level == 'info':
            logger = self.logger.info
        else:
            logger =  self.logger.debug
        for line in output:
            line = line.rstrip()
            if len(line):
                if error_substring is not None and error_substring in line:
                    raise CommandError(line)
                logger(line)
        return



class TestConfigure(unittest.TestCase):
    """
    Tests the Configure context manager
    """
    def setUp(self):
        self.connection = MagicMock()
        self.interface = 'ath0'
        self.logger = MagicMock()
        self.configure = Configure(connection=self.connection,
                                   interface=self.interface)
        self.configure._logger = self.logger
        return

    def set_context_connection(self):
        self.connection.apdown.return_value = EMPTY_TUPLE
        self.connection.cfg.return_value = EMPTY_TUPLE
        self.connection.apup.return_value = EMPTY_TUPLE
        return

    def test_constructor(self):
        """
        Does the configure have the right constructor?
        """
        self.assertEqual(self.connection, self.configure.connection)
        self.assertEqual(self.configure.interface, self.interface)
        return

    def test_enter(self):
        """
        Does the context manager take down the ap?
        """
        self.connection.apdown.return_value = ('', '')
        with Configure(self.connection, 'ath0') as c:
            pass
        self.connection.apdown.assert_called_with()
        return

    def test_exit(self):
        """
        Does the context manager commit the configuration and bring the AP up?
        """
        self.connection.apdown.return_value = ('', '')
        self.connection.cfg.return_value = ('','')
        self.connection.apup.return_value = ('','')
        
        with Configure(self.connection, 'ath0') as c:
            self.assertEqual(self.connection, c)
        calls = [call.apdown(), call.cfg('-c'), call.apup(),
                 call.wlanconfig("ath1 destroy")]
        self.assertEqual(calls, self.connection.method_calls)
        return

    def test_other_interface(self):
        """
        Does the correct interface get called
        """
        empty_tuple = ('', '')
        self.connection.apdown.return_value = empty_tuple
        self.connection.cfg.return_value = empty_tuple
        self.connection.apup.return_value = empty_tuple

        with Configure(self.connection, 'ath1'):
            pass

        self.connection.wlanconfig.assert_called_with('ath0 destroy')        
        return

    @raises(CommandError)
    def test_bad_interface(self):
        """
        Does the context manager raise a CommandError if it doesn't recognize the interface? 
        """
        self.set_context_connection()
        with Configure(self.connection, 'eth0'):
            pass
        return


class TestAtheros24(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.ap = Atheros24()
        self.ap._connection = self.connection
        self.ap._logger = MagicMock()
        self.enter_calls = [call.apdown()]
        self.exit_calls = [call.cfg('-c'), call.apup(),
                           call.wlanconfig("ath1 destroy")]   
        return
    
    def set_context_connection(self):
        self.connection.apdown.return_value = EMPTY_TUPLE
        self.connection.cfg.return_value = EMPTY_TUPLE
        self.connection.apup.return_value = EMPTY_TUPLE
        return

    def test_set_channel(self):
        """
        Does the ap configure set the channel correctly?
        """
        channel = 11
        self.set_context_connection()
        self.ap.set_channel(channel)
        calls = self.enter_calls + [call.cfg('-a AP_CHMODE=11HT20'),
                                    call.cfg('-a AP_PRIMARY_CH={0}'.format(channel)),
                                    call.cfg('-a AP_RADIO_ID=0')] + self.exit_calls
        self.assertEqual(calls, self.connection.method_calls)
        return
