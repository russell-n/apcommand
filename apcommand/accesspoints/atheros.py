
# python standard library
from abc import ABCMeta, abstractproperty, abstractmethod
import string
# this package
from apcommand.baseclass import BaseClass
from apcommand.connections.telnetconnection import TelnetConnection
from apcommand.commons.errors import CommandError
from apcommand.commons.errors import ArgumentError


EMPTY_STRING = ''
FIVE_GHZ_SUFFIX = '_2'
BAND_ID = {'2.4':0, '5':1}


class LineLogger(BaseClass):
    """
    Class to log lines of output
    """
    def __init__(self):
        """
        LineLogger constructor
        """
        super(LineLogger, self).__init__()
        return

    def __call__(self, output, error_substring=None, level='debug'):
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
        self._log_lines = None
        return

    @property
    def log_lines(self):
        """
        A LineLogger to log lines of output

        :return: line-logging object
        """
        if self._log_lines is None:
            self._log_lines = LineLogger()
        return self._log_lines

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

    def status(self, interface='ath0'):
        """
        Check iwconfig and ifconfig for the interface (set to 'all' to get all interfaces)

        :param:

         - `interface`: name of network interface (e.g. ath0)
        """
        if interface == 'all':
            interface = ''
        try:
            output, error = self.connection.iwconfig(interface)
            self.log_lines(output, level='info', error_substring='No such device')
            output, error = self.connection.ifconfig("{0} | grep 'inet addr'".format(interface))
            self.log_lines(output, level='info', error_substring='Device not found')
            output, error = self.connection.iwlist("{0} channel | grep Current".format(interface))
            self.log_lines(output, level='info')
        except CommandError:
                self.logger.info("interface {0} seems to be down".format(interface))
        return

    def reset(self, band='2.4'):
        """
        Clears the AP configuration back to the factory defaults

        :param:

         - `band`: 2.4 or 5
        """
        radio = BAND_ID[band]
        with Configure(connection=self.connection, radio_id=radio):
            output, error = self.connection.cfg('-x')
            self.log_lines(output)
        return

    def set_ssid(self, band, ssid):
        """
        Sets the SSID

        :param:

         - `band`: 2.4 or 5 (for GHz)
         - `ssid`: string name to set the ssid to 
        """
        with Configure(self.connection, radio_id=BAND_ID[band]):
            output, error = self.connection.cfg('-a AP_SSID={0}'.format(ssid))
        return

    def set_channel(self, channel, mode=None, bandwidth=None):
        """
        Sets the channel on the AP

        :param:

         - `channel`: A valid 802.11 channel
         - `mode`: optional mode (e.g. 11NG)
         - `bandwidth`: bandwidth for the mode (e.g. HT40PLUS)
        """
        changer = AtherosChannelChanger(connection=self.connection)
        changer(channel, mode, bandwidth)
        return

    def set_security(self, security_type='open'):
        """
        Set the security on the access point

        :param:

         - `security_type`: one of {open, WEP, WPA, WPA2}
        """
        if security_type == 'open':
            setter_class = AtherosOpen
        setter = setter_class(connection=self.connection)
        setter()
        return


class AtherosSecuritySetter(BaseClass):
    """
    A base-class to change the AP's security
    """
    __metaclass__ = ABCMeta
    def __init__(self, connection):
        """
        AtherosSecuritySetter Constructor

        :param:

         - `connection`: connection to the AP
        """
        super(AtherosSecuritySetter, self).__init__()
        self._logger = None
        self.connection = connection
        self._log_lines = None
        return

    @property
    def log_lines(self):
        """
        A logger to get lines from output and log them
        """
        if self._log_lines is None:
            self._log_lines = LineLogger()
        return self._log_lines

    @abstractmethod
    def __call__(self):
        """
        The main interface to the changers
        """
        return


class AtherosOpen(AtherosSecuritySetter):
    """
    Setter for open-security
    """
    def __init__(self, *args, **kwargs):
        """
        AtherosOpen constructor
        """
        super(AtherosOpen, self).__init__(*args, **kwargs)
        return

    def __call__(self):
        """
        sets the security mode to open
        """
        self.logger.debug('setting the security to open')
        with Configure(connection=self.connection):
            out, err = self.connection.cfg('-a AP_SECMODE=None')
            self.log_lines(out)
        return


class AtherosChannelChanger(BaseClass):
    """
    A channel changer
    """
    def __init__(self, connection):
        """
        AtherosChannelChanger constructor

        :param:

         - `connection`: the connection to the AP
        """
        super(AtherosChannelChanger, self).__init__()
        self.connection = connection
        self._logger = None
        self._g_channels = None
        self._a_channels = None
        self._log_lines = None
        return

    @property
    def log_lines(self):
        """
        A logger of lines
        """
        if self._log_lines is None:
            self._log_lines = LineLogger()
        return self._log_lines

    def bandwidth(self, channel):
        """
        Gets a mode appropriate for the channel, based on T/H's defaults

        :param:

         - `channel`: integer (or string) WiFi channel (e.g. 11)

        :return: string of form 'HT(20|40)[MINUS|PLUS]
        :raise: ArgumentError if invalid (DFS channels not allowed)
        """
        channel = str(channel)
        if channel in self.g_channels:
            # assume 11NGHT20 only allowed setting
            return "HT20"
        edges = "48 61".split()
        if channel in edges:
            # upper limits of bands
            return "HT40MINUS"
        elif channel in self.a_channels:
            return "HT40PLUS"
        else:
            raise ArgumentError("Invalid Channel: {0}".format(channel))
        return

    def mode(self, channel):
        """
        The mode appropriate for the channel (e.g. 11NA)

        :param:

         - `channel`: 2.4 GHz or 5GHz channels

        :return: string of the form `11N(G|A)`
        :raises: ArgumentError if channel invalid (DFS considered invalid too)
        """
        if str(channel) in self.g_channels:
            return "11NG"
        elif str(channel) in self.a_channels:
            return '11NA'
        else:
            raise ArgumentError("Invalid Channel ({0})".format(channel))
        return

    def parameter_suffix(self, channel):
        """
        The suffix for cfg -a parameter names

        :return: (''|'_2')
        :raises: ArgumentError for invalid channel
        """
        channel = str(channel)
        if channel in self.g_channels:
            return EMPTY_STRING
        if channel in self.a_channels:
            return FIVE_GHZ_SUFFIX
        raise ArgumentError("Invalid Channel: {0}".format(channel))
        return 

    @property
    def g_channels(self):
        """
        a list of valid channels
        """
        if self._g_channels is None:
            self._g_channels = [str(channel) for channel in range(1,12)]
        return self._g_channels

    @property
    def a_channels(self):
        if self._a_channels is None:
            set_1 = [str(i) for i in range(36,49,4)]
                # Henry W says to ignore DFS Channels
                #set_2 = [str(j) for j in range(100,141,4)]
            set_3 = [str(k) for k in range(149,166,4)]
            self._channels = set_1 + set_3
        return self._channels

    def __call__(self, channel, mode=None, bandwidth=None):
        """
        method to set the channel on the AP

        :param:

         - `channel`: string or integer in valid_channels
         - `mode`: 11NA, 11NG, 11A, 11G, 11B
         - `bandwidth`: HT20, HT40, HT40PLUS, HT40MINUS (valid for mode)
        """
        channel = str(channel)
        if mode is None:
            mode = self.mode(channel)
        mode = mode.upper()
        if bandwidth is None:
            bandwidth = self.bandwidth(channel)

        parameter_suffix = self.parameter_suffix(channel)
        with Configure(connection=self.connection):
            output, error = self.connection.cfg('-a AP_CHMODE{1}={0}HT20'.format(mode,
                                                                                 parameter_suffix))
            self.log_lines(output)
            output, error = self.connection.cfg('-a AP_PRIMARY_CH{1}={0}'.format(channel,
                                                                                 parameter_suffix))
            self.log_lines(output)
        return

    def validate_channel(self, channel):
        """
        Check to see if the channel is acceptible

        :raises: ArgumentError if not a valid 2.4 GHz channel
        """
        if channel not in self.channels:
            raise ArgumentError("Invalid Channel: {0}".format(channel))
        return


class Atheros24Ghz(AtherosChannelChanger):
    """
    A channel-changer for 2.4 GHz
    """
    def __init__(self, *args, **kwargs):
        """
        Atheros24GHz constructor
        """
        super(Atheros24Ghz, self).__init__(*args, **kwargs)
        return

    @property
    def interface(self):
        """
        The name of the VAP (ath0)
        """
        if self._interface is None:
            self._interface = 'ath0'
        return self._interface



class Atheros5GHz(AtherosChannelChanger):
    """
    A channel-changer for 5 GHz
    """
    def __init__(self, *args, **kwargs):
        """
        Atheros5GHz constructor
        """
        super(Atheros5GHz, self).__init__(*args, **kwargs)
        return



# python standard library
import unittest
import random
# third party
from mock import MagicMock, call, patch
from nose.tools import raises


ENTER_CALLS = [call.apdown(), call.cfg('-a AP_RADIO_ID=0'),
               call.cfg('-a AP_STARTMODE=standard')]
EXIT_CALLS = [call.cfg('-c'), call.apup()]



EMPTY_TUPLE = ('','')

class TestAR5KAP(unittest.TestCase):
    def setUp(self):
        self.logger = MagicMock()
        self.connection = MagicMock()
        self.ap = AtherosAR5KAP()
        self.ap._connection = self.connection
        self.ap._logger = self.logger
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
        #self.assertRaises(CommandError, self.ap.status, ['ath0'])
        return

    def test_ifconfig_fail(self):
        """
        Does a missing interface not raise an error?
        """
        self.connection.iwconfig.return_value = ('','')
        self.connection.ifconfig.return_value = (['ifconfig: ath0: error fetching interface information: Device not found\n'], '')
        self.connection.iwlist.return_value = ('','')
        #self.assertRaises(CommandError, self.ap.status, ['ath0'])
        return

    def test_reset(self):
        """
        Does the reset clear the configuration?
        """
        self.set_context_connection()
        self.ap.reset(band='2.4')
        calls = ENTER_CALLS + [call.cfg('-x')] + EXIT_CALLS
        self.assertEqual(calls, self.connection.method_calls)
        return

    def test_set_ssid(self):
        """
        Does the control set the ssid correctly?
        """
        self.set_context_connection()        
        ssid = ''.join((random.choice(string.printable) for choice in range(random.randrange(100))))
        self.ap.set_ssid(band='2.4', ssid=ssid)
        calls = ENTER_CALLS + [call.cfg('-a AP_SSID={0}'.format(ssid))] + EXIT_CALLS
        self.assertEqual(calls, self.connection.method_calls)
        return

    def test_set_channel_24(self):
        """
        Does the controller get the right channel changer and call it?
        """
        self.set_context_connection()
        channel = random.randrange(1,12)
        changer = MagicMock()
        changer_call = MagicMock()
        changer.__call__ = changer_call
        with patch('apcommand.accesspoints.atheros.AtherosChannelChanger', changer):
            self.ap.set_channel(channel)

        changer.assert_called_with(connection=self.connection)
        return 

    def test_set_channel_5(self):
        """
        Does the controller get the right (5GHz) channel changer and call it?
        """
        self.set_context_connection()
        set_1 = [str(i) for i in range(36,65,4)]
        set_2 = [str(j) for j in range(100,141,4)]
        set_3 = [str(k) for k in range(149,166,4)]
        channels = set_1 + set_2 + set_3
        channel = random.choice(channels)
        changer = MagicMock()
        with patch('apcommand.accesspoints.atheros.AtherosChannelChanger', changer):
            self.ap.set_channel(channel)
        changer.assert_called_with(connection=self.connection)
        return

    def test_set_security(self):
        """
        Does the controller get the right setter and call it?
        """
        self.set_context_connection()
        security_type = 'open'
        setter = MagicMock()
        with patch('apcommand.accesspoints.atheros.AtherosOpen', setter):
            self.ap.set_security(security_type=security_type)
        setter.assert_called_with(connection=self.connection)
        calls = ENTER_CALLS + [call.cfg('-a AP_SECMODE=None')] + EXIT_CALLS
        return


class Configure(BaseClass):
    """
    A context manager for configure commands on the Atheros
    """
    def __init__(self, connection, radio_id=0):
        """
        The Configure constructor 

        :param:

         - `connection`: connection to AP's command-line interface
         - `radio_id`: the id (0 for 2.4ghz 1 for 5GHz)
        """
        super(Configure, self).__init__()
        self.connection = connection
        self.radio_id = radio_id
        self._log_lines = None
        self.logger.debug(str(connection))
        self.logger.debug("radio id: {0}".format(radio_id))
        return

    @property
    def log_lines(self):
        """
        A logger of output lines
        """
        if self._log_lines is None:
            self._log_lines = LineLogger()
        return self._log_lines

    def __enter__(self):
        """
        Takes down the AP
        """
        # turn off the wifi interface
        output, error = self.connection.apdown()
        self.log_lines(output)
        # tell it which radio to set up (0=2.4GHz, 1=5GHz)
        output, error = self.connection.cfg('-a AP_RADIO_ID={0}'.format(self.radio_id))
        self.log_lines(output)
        # tell it to only start up the current radio, not both ath0 and ath1
        output, error = self.connection.cfg('-a AP_STARTMODE=standard')
        self.log_lines(output)
        return self.connection

    def __exit__(self, type, value, traceback):
        """
        Commits the configuration and brings up the AP, destroying the other VAP
        """
        # commit the configuration changes        
        output, error = self.connection.cfg('-c')
        self.log_lines(output)
        # bring up the AP
        output, error = self.connection.apup()
        self.log_lines(output)
        return    


class TestConfigure(unittest.TestCase):
    """
    Tests the Configure context manager
    """
    def setUp(self):
        self.connection = MagicMock()
        self.radio_id = '2.4'
        self.logger = MagicMock()
        self.configure = Configure(connection=self.connection,
                                   radio_id=self.radio_id)
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
        self.assertEqual(self.configure.radio_id, self.radio_id)
        return

    def test_enter(self):
        """
        Does the context manager take down the ap?
        """
        self.set_context_connection()
        with Configure(self.connection, 'ath0') as c:
            pass
        self.connection.apdown.assert_called_with()
        return

    def test_exit(self):
        """
        Does the context manager commit the configuration and bring the AP up?
        """
        self.set_context_connection()
        
        with Configure(self.connection, 0) as c:
            self.assertEqual(self.connection, c)
        calls = [call.apdown(), call.cfg('-a AP_RADIO_ID=0'),
                 call.cfg('-a AP_STARTMODE=standard'),
                 call.cfg('-c'), call.apup()]
                 #call.wlanconfig("ath1 destroy")]
        self.assertEqual(calls, self.connection.method_calls)
        return

    #def test_other_interface(self):
    #    """
    #    Does the correct interface get called
    #    """
    #    self.set_context_connection()
    #    with Configure(self.connection, 'ath1'):
    #        pass
    #
    #    self.connection.wlanconfig.assert_called_with('ath0 destroy')        
    #    return

    #@raises(CommandError)
    #def test_bad_interface(self):
    #    """
    #    Does the context manager raise a CommandError if it doesn't recognize the interface? 
    #    """
    #    self.set_context_connection()
    #    with Configure(self.connection, 'eth0'):
    #        pass
    #    return


class TestAtheros24(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.changer = Atheros24Ghz(self.connection)
        self.logger = MagicMock()
        self.changer._logger = self.logger
        return
    
    def set_context_connection(self):
        self.connection.apdown.return_value = EMPTY_TUPLE
        self.connection.cfg.return_value = EMPTY_TUPLE
        self.connection.apup.return_value = EMPTY_TUPLE
        return

    def g_channel(self):
        return random.randrange(1, 12)

    def bad_channel(self):
        return random.randrange(12, 36)

    def test_bandwidth(self):
        """
        Does the changer get an appropriate bandwidth for the channel?
        """
        channel = self.g_channel()
        bandwidth = self.changer.bandwidth(channel)
        self.assertEqual('HT20', bandwidth)
        self.assertRaises(ArgumentError, self.changer.bandwidth, self.bad_channel())
        return

    def test_parameter_suffix(self):
        """
        Does the changer get the appropriate parameter suffix for the channel?
        """
        channel = self.g_channel()
        suffix = self.changer.parameter_suffix(channel)
        self.assertEqual(EMPTY_STRING, suffix)
        self.assertRaises(ArgumentError, self.changer.parameter_suffix,
                          self.bad_channel())
        return

    def test_mode(self):
        """
        Does the mode method get the right mode based on the channel?
        """
        channel = self.g_channel()
        mode = self.changer.mode(str(channel))
        self.assertEqual(mode, '11NG')
        self.assertRaises(ArgumentError,
                          self.changer.mode,
                          self.bad_channel())
        return
    
    def test_set_channel(self):
        """
        Does the ap configure set the channel correctly?
        """
        channel = self.g_channel()
        self.set_context_connection()
        self.changer(channel)
        calls = ENTER_CALLS + [call.cfg('-a AP_CHMODE=11NGHT20'),
                                    call.cfg('-a AP_PRIMARY_CH={0}'.format(channel))] + EXIT_CALLS
    
    #    print self.logger.method_calls
        self.assertEqual(calls, self.connection.method_calls)
        return


class TestAtheros5GHz(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.changer = Atheros5GHz(self.connection)
        self.changer._logger = MagicMock()
        self.enter_calls = [call.apdown(), call.cfg('-a AP_RADIO_ID=1'),
               call.cfg('-a AP_STARTMODE=standard')]
        return
    
    def set_context_connection(self):
        self.connection.apdown.return_value = EMPTY_TUPLE
        self.connection.cfg.return_value = EMPTY_TUPLE
        self.connection.apup.return_value = EMPTY_TUPLE
        return

    def dfs_channel(self):
        return random.choice([str(j) for j in range(100,141,4)])

    def a_channel(self):
        return random.choice([str(i) for i in range(36,49,4)] +
                            [str(k) for k in range(149,166,4)])

    def test_bandwidth(self):
        """
        Does the changer select the correct 5ghz bandwidth?
        """
        channel = self.a_channel()
        bandwidth = self.changer.bandwidth(channel)
        if channel in '48 61'.split():
            self.assertEqual("HT40MINUS", bandwidth)
        else:
            self.assertEqual("HT40PLUS", bandwidth)
        channel = self.dfs_channel()
        self.assertRaises(ArgumentError, self.changer.bandwidth, channel)
        return

    def test_parameter_suffix(self):
        """
        Does the changer return the cfg -a parameter suffix for 5GHZ?
        """
        channel = self.a_channel()
        suffix = self.changer.parameter_suffix(channel)
        self.assertEqual("_2", suffix)
        channel = self.dfs_channel()
        self.assertRaises(ArgumentError, self.changer.parameter_suffix, channel)
        return

    def test_mode(self):
        """
        Does the changer return the default 5GHz mode?
        """
        channel = self.a_channel()
        mode = self.changer.mode(str(channel))                                 
        self.assertEqual(mode, '11NA')
        channel = self.dfs_channel()
        self.assertRaises(ArgumentError, self.changer.mode, str(channel))
        return

        
    def test_set_channel(self):
        """
        Does the ap configure set the channel correctly?
        """
        channel = self.a_channel()
    #    self.set_context_connection()
    #    self.ap(channel)
    #    calls = self.enter_calls + [call.cfg('-a AP_CHMODE_2=11naHT20'),
    #                                call.cfg('-a AP_PRIMARY_CH_2={0}'.format(channel))] + EXIT_CALLS
    #    self.assertEqual(calls, self.connection.method_calls)
    #    return

    #def test_validate_channel(self):
    #    """
    #    Does the changer raise an ArgumentError for an invalid channel?"
    #    """
    #    channel = str(random.randint(166,200))
    #    self.assertRaises(ArgumentError, self.ap.validate_channel, [channel])
    #    self.ap.validate_channel(str(random.randrange(36,65,4)))
    #    return


class TestAtherosOpen(unittest.TestCase):
    def set_context_connection(self):
        self.connection.apdown.return_value = EMPTY_TUPLE
        self.connection.cfg.return_value = EMPTY_TUPLE
        self.connection.apup.return_value = EMPTY_TUPLE
        return

    def setUp(self):
        self.connection = MagicMock()
        self.setter = AtherosOpen(connection=self.connection)
        return

    def test_call(self):
        """
        Does the __call__ issue the correct commands?
        """
        self.set_context_connection()
        self.setter()
        return
