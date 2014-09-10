
#python standard library
import re
import os

#this package
import apcommand.commons.oatbran as oatbran
from apcommand.commons.errors import CommandError
from apcommand.baseclass import BaseClass


class IwconfigEnums(object):
    __slots__ = ()
    ssid = "ssid"
    bssid = "bssid"
    rssi = "rssi"
    noise = 'noise'
    bitrate = 'bitrate'
    frequency = 'frequency'
    protocol = 'protocol'
    interface = 'interface'
# end class IwconfigEnums


class IwconfigCommand(BaseClass):
    '''
    a class to bundle the connection and the iperf lexer
    '''
    def __init__(self, connection, interface='wlan0', not_available="NA"):
        """
        IwconfigCommand constructor

        :param:

         - `connection`: connection to the device
         - `interface`: name of the interface (e.g. eth0)
         - `not_available`: string to return if the information is N/A
        """
        super(IwconfigCommand, self).__init__()
        self.connection = connection
        self.interface = interface
        self.not_available = not_available
        self._lexer = None
        self._bitrate = None
        self._ssid = None
        self._rssi = None
        self._noise = None
        self._bssid = None
        self._found_interface = None
        self._frequency = None
        self._protocol = None
        return

    @property
    def lexer(self):
        """
        A lexer for the iwconfig output
        """
        if self._lexer is None:
            self._lexer = IwconfigLexer(interface=self.interface)
        return self._lexer

    @property
    def bitrate(self):
        """
        Gets the bitrate 
        """
        output = self.output()
    
        return self.lexer.search(lines=output.output,
                                 expression=self.lexer.bitrate,
                                 name=IwconfigEnums.bitrate)

    @property
    def ssid(self):
        """
        Gets the interface ssid (discovered, not passed to constructor)
        """
        return self.lexer.search(lines=self.output().output,
                                 expression=self.lexer.ssid,
                                 name=IwconfigEnums.ssid)

    @property
    def rssi(self):
        """
        the interface's rssi
        """
        return self.lexer.search(lines=self.output().output,
                                 expression=self.lexer.rssi,
                                 name=IwconfigEnums.rssi)

    @property
    def noise(self):
        """
        the interface noise
        """
        return self.lexer.search(lines=self.output().output,
                                 expression=self.lexer.noise,
                                 name=IwconfigEnums.noise)

    @property
    def bssid(self):
        """
        the BSSID (MAC Address) of the interface
        """
        return self.lexer.search(lines=self.output().output,
                                 expression=self.lexer.bssid,
                                 name=IwconfigEnums.bssid)

    @property
    def found_interface(self):
        """
        the interface in the iwconfig output string
        """
        return self.lexer.search(lines=self.output().output,
                                 expression=self.lexer.found_interface,
                                 name=IwconfigEnums.interface)

    @property
    def frequency(self):
        """
        The frequency of the interface       
        """
        return self.lexer.search(lines=self.output().output,
                                 expression=self.lexer.frequency,
                                 name=IwconfigEnums.frequency)

    @property
    def protocol(self):
        """
        the protocol for the interface 
        """
        return self.lexer.search(lines=self.output().output,
                                 expression=self.lexer.protocol,
                                 name=IwconfigEnums.protocol)

    def output(self):
        """
        Calls the `iwconfig <interface>` command on the self.connection

        :rtype: namedtuple
        :return: output of the connection
        """
        return self.connection.iwconfig(self.interface)

    def __str__(self):
        return """
        SSID: {s}
        BSSID: {b}
        RSSI: {r}
        Noise: {n}
        Bit Rate: {br}
        Frequency: {f}
        Protocol: {p}
        Interface: {i}
        """.format(s=self.ssid,
                   b=self.bssid,
                   r=self.rssi,
                   n=self.noise,
                   br=self.bitrate,
                   f=self.frequency,
                   p=self.protocol,
                   i=self.found_interface)
        

# end class IwconfigCommand


class IwconfigLexer(object):
    """
    A class to extract `iwconfig` information
    """
    def __init__(self, interface="wlan0", not_available="NA"):
        """
        Iwconfig constructor
        
        :param:

         - `interface`: the name of the wireless interface
         - `not_available`: token to return if the field isn't found
        """
        self.interface = interface
        self.not_available = not_available
        self._ssid = None
        self._bssid = None
        self._rssi = None
        self._noise = None
        self._bitrate = None
        self._frequency = None
        self._frequency = None
        self._protocol = None
        self._found_interface = None
        return

    @property
    def found_interface(self):
        """
        Named regular expression to match the found_interface
        """
        if self._found_interface is None:
            self._found_interface = re.compile(oatbran.Boundaries.string_start + 
                                                    oatbran.Group.named(name=IwconfigEnums.interface,
                                                                  expression=oatbran.CommonPatterns.letters + oatbran.Numbers.integer))
        return self._found_interface

    @property
    def protocol(self):
        """
        Expression to extract the protocol (e.g. 'na' from 'IEEE 802.11na')

        :return: compiled regular expression with named expression IwconfigEnums.protocol
        """
        if self._protocol is None:
            self._protocol = re.compile("IEEE" + oatbran.CommonPatterns.spaces + r'802\.11' +
                                                    oatbran.Group.named(name=IwconfigEnums.protocol,
                                                                  expression=oatbran.CharacterClass.character_class('abgn')+
                                                                  oatbran.Quantifier.one_or_more))
        return self._protocol

    @property
    def frequency(self):
        """
        Named expression to match the frequency
        """
        if self._frequency is None:
            self._frequency = re.compile("Frequency" + oatbran.CommonPatterns.optional_spaces + r'(:|=)' +
                                                    oatbran.CommonPatterns.optional_spaces + 
                                                    oatbran.Group.named(name=IwconfigEnums.frequency,
                                                                  expression=oatbran.Numbers.real) + oatbran.CommonPatterns.spaces + 'GHz')
        return self._frequency

    
    @property
    def bitrate(self):
        if self._bitrate is None:
	   self._bitrate = re.compile("Bit" + oatbran.CommonPatterns.spaces + 
                                                  "Rate" + oatbran.CommonPatterns.optional_spaces + r'(:|=)' +
                                                  oatbran.CommonPatterns.optional_spaces + 
                                                  oatbran.Group.named(name=IwconfigEnums.bitrate,
                                                                expression=oatbran.Numbers.integer + oatbran.CommonPatterns.everything + 'b/s') +
                                                  oatbran.CommonPatterns.spaces)
        return self._bitrate

    @property
    def noise(self):
        if self._noise is None:
            self._noise = re.compile("Noise" + oatbran.CommonPatterns.spaces + 
                                               "level" + oatbran.CommonPatterns.optional_spaces + '=' +
                                               oatbran.CommonPatterns.optional_spaces + 
                                               oatbran.Group.named(name=IwconfigEnums.noise,
                                                             expression='-' + oatbran.Number.integer)+
                                               oatbran.CommonPattern.spaces + 'dBm')
        return self._noise

    @property
    def rssi(self):
        """
        :return: compiled regular expression to match the rssi value
        """
        if self._rssi is None:
            self._rssi = re.compile("Signal" + oatbran.CommonPatterns.spaces + "level"+
                                               oatbran.CommonPatterns.optional_spaces + "=" +
                                               oatbran.CommonPatterns.optional_spaces +
                                               oatbran.Group.named(name=IwconfigEnums.rssi,
                                                             expression=oatbran.Numbers.integer) +
                                               oatbran.CommonPatterns.spaces + "dBm")
        return self._rssi
    
    @property
    def ssid(self):
        """
        :return: compiled regular expression to match the SSID
        """
        if self._ssid is None:
            self._ssid = re.compile(r'ESSID:\"{0}\"'.format(oatbran.Group.named(name=IwconfigEnums.ssid,
                                                                                     expression='[^"]' + oatbran.Quantifier.one_or_more)))
        return self._ssid

    @property
    def bssid(self):
        """
        :return: compiled regular expression to match the BSSID
        """
        if self._bssid is None:
            self._bssid = re.compile("Access" + oatbran.CommonPatterns.spaces + "Point:" + oatbran.CommonPatterns.spaces +
                                                oatbran.Group.named(name=IwconfigEnums.bssid,
                                                              expression=oatbran.Networking.mac_address))
        return self._bssid
    
    def search(self, lines, expression, name):
        """
        searches lines for the expression
        
        :param:

         - `lines`: iterable output of iwconfig command
         - `expression`: regular expression to match desired field
         - `name`: the name of the group in the expression to return

        :return: matched sub-string or not_available
        """
        for line in lines:
            match = expression.search(line)
            if match:
                return match.groupdict()[name]
            self.validate(line)
        return self.not_available
        
    def validate(self, line):
        """
        Checks the line for 'No such device'
        
        :param:

         - `line`: A string of output from the `iwconfig` command

        :raise: CommandError if the interface wasn't found
        """
        if "No such device" in line:
            raise CommandError(line)
        return


# end class IwconfigLexer


# python standard library
import unittest

# third-party
from mock import MagicMock

# this package
from apcommand.commons.randomizer import Randomizer
from apcommand.connections.nonlocalconnection import OutputError


EMPTY_TUPLE = ('','')
sample_output="""
iwconfig ath0
ath0      IEEE 802.11ng  ESSID:"whentwovowelsgoawalking"
          Mode:Master  Frequency:2.462 GHz  Access Point: 00:03:7F:12:3A:0F
          Bit Rate:130 Mb/s   Tx-Power:15 dBm
          RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:off
          Link Quality=63/94  Signal level=-72 dBm  Noise level=-95 dBm
          Rx invalid nwid:26742  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:0  Invalid misc:0   Missed beacon:0
""".split('\n')
SAMPLE_BITRATE = '130 Mb/s'
SAMPLE_SSID = 'whentwovowelsgoawalking'
SAMPLE_RSSI = '-72'
SAMPLE_NOISE = '-95'
SAMPLE_MAC = '00:03:7F:12:3A:0F'
SAMPLE_FREQUENCY = '2.462'
SAMPLE_PROTOCOL = 'ng'
SAMPLE_INTERFACE = 'ath0'


class TestIwconfig(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.interface = Randomizer.random_letters(maximum=3) + str(Randomizer.random_integer())
        self.na = Randomizer.random_string()
        self.iwconfig = IwconfigCommand(connection=self.connection,
                                 interface=self.interface,
                                 not_available=self.na)
        return

    def test_constructor(self):
        """
        Does the constructor take the expected arguments?
        """
        self.assertEqual(self.connection, self.iwconfig.connection)
        self.assertEqual(self.na, self.iwconfig.not_available)
        self.assertEqual(self.interface, self.iwconfig.interface)
        return

    def setup_sample_output(self):
        output, error = sample_output, ''
        o_e = OutputError(output, error)
        self.connection.iwconfig.return_value = o_e
        return
    
    def test_bitrate(self):
        """
        Does the iwconfig make the correct call to the connection?
        """
        self.setup_sample_output()
        bitrate = self.iwconfig.bitrate
        self.connection.iwconfig.assert_called_with(self.interface)
        self.assertEqual(SAMPLE_BITRATE, bitrate)
        return
    
    def test_ssid(self):
        """
        Dose it get the sample SSID?
        """
        self.setup_sample_output()
        ssid = self.iwconfig.ssid
        self.assertEqual(SAMPLE_SSID, ssid)
        return
    
    def test_rssi(self):
        """
        Does it get the correct RSSI?
        """
        self.setup_sample_output()
        rssi = self.iwconfig.rssi
        self.assertEqual(SAMPLE_RSSI, rssi)
        return
    
    def test_noise(self):
        """
        Does it get the correct noise?
        """
        self.setup_sample_output()
        noise = self.iwconfig.noise
        self.assertEqual(SAMPLE_NOISE, noise)
        return
    
    def test_bssid(self):
        """
        Does it get the right MAC Address?
        """
        self.setup_sample_output()
        bssid = self.iwconfig.bssid
        self.assertEqual(SAMPLE_MAC, bssid)
        return
    
    def test_frequency(self):
        """
        Does it get the right frequency?
        """
        self.setup_sample_output()
        frequency = self.iwconfig.frequency
        self.assertEqual(SAMPLE_FREQUENCY, frequency)
        return
    
    
    def test_protocol(self):
        """
        Does it get the protocol?
        """
        self.setup_sample_output()
        protocol = self.iwconfig.protocol
        self.assertEqual(SAMPLE_PROTOCOL, protocol)
        return
    

    def test_interface(self):
        """
        Does it match the interface string?
        """
        self.setup_sample_output()
        interface = self.iwconfig.found_interface
        self.assertEqual(SAMPLE_INTERFACE, interface)
        return



class TestIwconfigLexer(unittest.TestCase):
    def setUp(self):
        self.iwconfig = IwconfigLexer()
        return

    def test_frequency(self):
        """
        Does the expression match the frequency?
        """
        example = 'Frequency:2.437 GHz'
        self.assertRegexpMatches(example, self.iwconfig.frequency)
        return
    
    def test_protocol(self):
        """
        Does the expression match the protocol?
        """
        sample = "IEEE 802.11bgn"
        self.assertRegexpMatches(sample, self.iwconfig.protocol)
        return
    
    def test_interface(self):
        """
        Does it match the interface string?
        """
        sample = 'ath0 IEEE 802.11ng ESSID:ath0ap'
        self.assertRegexpMatches(sample, self.iwconfig.found_interface)
        self.assertNotRegexpMatches('ESSID:ath0', self.iwconfig.found_interface)
        return
    
