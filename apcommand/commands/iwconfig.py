
#python standard library
import re
import os

#this package
import apcommand.commons.oatbran as oatbran
from apcommand.commons.errors import CommandError


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


class IwconfigLexer(object):
    """
    A class to extract `iwconfig` information
    """
    def __init__(self, connection, interface="wlan0", not_available="NA"):
        """
        Iwconfig constructor
        
        :param:

         - `connection`: A connection to the device
         - `interface`: the name of the wireless interface
         - `not_available`: token to return if the field isn't found
        """
        self.connection = connection
        self.interface = interface
        self.not_available = not_available
        self._ssid = None
        self._ssid_expression = None
        self._bssid = None
        self._bssid_expression = None
        self._rssi = None
        self._rssi_expression = None
        self._noise_expression = None
        self._bitrate = None
        self._bitrate_expression = None
        self._noise = None
        self._frequency_expression = None
        self._frequency = None
        self._frequency_expression = None
        self._frequency = None
        self._protocol_expression = None
        self._protocol = None
        self._interface_expression = None
        self._found_interface = None        
        return

    @property
    def interface_expression(self):
        """
        Named regular expression to match the interface
        """
        if self._interface_expression is None:
            self._interface_expression = re.compile(oatbran.STRING_START + 
                                                    oatbran.NAMED(n=IwconfigEnums.interface,
                                                                  e=oatbran.LETTERS + oatbran.NATURAL))

        return self._interface_expression

    @property
    def found_interface(self):
        """
        Interface sub-string matched by protocol_expression (it is `found` not value passed in)
        """
        return self.search(self.interface_expression, IwconfigEnums.interface)

    @property
    def protocol_expression(self):
        """
        Expression to extract the protocol (e.g. 'na' from 'IEEE 802.11na')

        :return: compiled regular expression with named expression IwconfigEnums.protocol
        """
        if self._protocol_expression is None:
            self._protocol_expression = re.compile("IEEE" + oatbran.SPACES + r'802\.11' +
                                                    oatbran.NAMED(n=IwconfigEnums.protocol,
                                                                  e=oatbran.CLASS('abgn')+
                                                                  oatbran.ONE_OR_MORE))
        return self._protocol_expression

    @property
    def protocol(self):
        """
        Protocol sub-string matched by protocol_expression
        """
        return self.search(self.protocol_expression, IwconfigEnums.protocol)

    @property
    def frequency_expression(self):
        if self._frequency_expression is None:
            self._frequency_expression = re.compile("Frequency" + oatbran.OPTIONAL_SPACES + r'(:|=)' +
                                                    oatbran.OPTIONAL_SPACES + 
                                                    oatbran.NAMED(n=IwconfigEnums.frequency,
                                                                  e=oatbran.REAL) + oatbran.SPACES + 'GHz')
        return self._frequency_expression

    @property
    def frequency(self):
        return self.search(self.frequency_expression, IwconfigEnums.frequency)
    
    @property
    def bitrate_expression(self):
        if self._bitrate_expression is None:
            self._bitrate_expression = re.compile("Bit" + oatbran.SPACES + 
                                                  "Rate" + oatbran.OPTIONAL_SPACES + r'(:|=)' +
                                                  oatbran.OPTIONAL_SPACES + 
                                                  oatbran.NAMED(n=IwconfigEnums.bitrate,
                                                                e=oatbran.INTEGER + oatbran.EVERYTHING + 'b/s') +
                                                  oatbran.SPACES)
        return self._bitrate_expression

    @property
    def bitrate(self):
        return self.search(self.bitrate_expression, IwconfigEnums.bitrate)



    @property
    def noise_expression(self):
        if self._noise_expression is None:
            self._noise_expression = re.compile("Noise" + oatbran.SPACES + 
                                               "level" + oatbran.OPTIONAL_SPACES + '=' +
                                               oatbran.OPTIONAL_SPACES + 
                                               oatbran.NAMED(n=IwconfigEnums.noise,
                                                             e='-' + oatbran.INTEGER)+
                                               oatbran.SPACES + 'dBm')
        return self._noise_expression

    @property
    def noise(self):
        return self.search(self.noise_expression, IwconfigEnums.noise)

    @property
    def rssi_expression(self):
        """
        :return: compiled regular expression to match the rssi value
        """
        if self._rssi_expression is None:
            self._rssi_expression = re.compile("Signal" + oatbran.SPACES + "level"+
                                               oatbran.OPTIONAL_SPACES + "=" +
                                               oatbran.OPTIONAL_SPACES +
                                               oatbran.NAMED(n=IwconfigEnums.rssi,
                                                             e=oatbran.INTEGER) +
                                               oatbran.SPACES + "dBm")
        return self._rssi_expression
    
    @property
    def rssi(self):
        return self.search(self.rssi_expression, IwconfigEnums.rssi)
    
    @property
    def ssid_expression(self):
        """
        :return: compiled regular expression to match the SSID
        """
        if self._ssid_expression is None:
            self._ssid_expression = re.compile(r'ESSID:\"{0}\"'.format(oatbran.NAMED(n=IwconfigEnums.ssid,
                                                                                     e='[^"]' + oatbran.ONE_OR_MORE)))
        return self._ssid_expression

    @property
    def bssid_expression(self):
        """
        :return: compiled regular expression to match the BSSID
        """
        if self._bssid_expression is None:
            self._bssid_expression = re.compile("Access" + oatbran.SPACES + "Point:" + oatbran.SPACES +
                                                oatbran.NAMED(n=IwconfigEnums.bssid,
                                                              e=oatbran.MAC_ADDRESS))
        return self._bssid_expression

    @property
    def bssid(self):
        """
        :return: the bssid or none
        """
        return self.search(self.bssid_expression, IwconfigEnums.bssid)
    
    @property
    def ssid(self):
        """
        :return: the ssid of the attached ap or not_available if not found
        """
        return self.search(self.ssid_expression, IwconfigEnums.ssid)

    def output(self):
        return self.connection.iwconfig(self.interface)                    

    def search(self, expression, name):
        """
        :param:

         - `expression`: regular expression to match desired field
         - `name`: the name of the group in the expression to return

        :return: matched sub-string or not_available
        """
        output = self.output()
        for line in output.output:
            match = expression.search(line)
            if match:
                return match.groupdict()[name]
            self.validate(line)
        return self.not_available
        
    def validate(self, line):
        """
        :param:

         - `line`: A string of output from the `iwconfig` command

        :raise: CommandError if the interface wasn't found
        """
        if "No such device" in line:
            raise CommandError(line)
        return

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
        
# end class Iwconfig


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
        self.iwconfig = IwconfigLexer(connection=self.connection,
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

    def test_frequency_expression(self):
        """
        Does the expression match the frequency?
        """
        example = 'Frequency:2.437 GHz'
        self.assertRegexpMatches(example, self.iwconfig.frequency_expression)
        return

    def test_frequency(self):
        """
        Does it get the right frequency?
        """
        self.setup_sample_output()
        frequency = self.iwconfig.frequency
        self.assertEqual(SAMPLE_FREQUENCY, frequency)
        return

    def test_protocol_expression(self):
        """
        Does the expression match the protocol?
        """
        sample = "IEEE 802.11bgn"
        self.assertRegexpMatches(sample, self.iwconfig.protocol_expression)
        return

    def test_protocol(self):
        """
        Does it get the protocol?
        """
        self.setup_sample_output()
        protocol = self.iwconfig.protocol
        self.assertEqual(SAMPLE_PROTOCOL, protocol)
        return

    def test_interface_expression(self):
        """
        Does it match the interface string?
        """
        sample = 'ath0 IEEE 802.11ng ESSID:ath0ap'
        self.assertRegexpMatches(sample, self.iwconfig.interface_expression)
        self.assertNotRegexpMatches('ESSID:ath0', self.iwconfig.interface_expression)
        return

    def test_interface(self):
        """
        Does it match the interface string?
        """
        self.setup_sample_output()
        interface = self.iwconfig.found_interface
        self.assertEqual(SAMPLE_INTERFACE, interface)
        return



if __name__ == '__main__':
    connection = MagicMock()
    iwconfig = IwconfigLexer(connection=connection)
    output, error = sample_output, ''
    o_e = OutputError(output, error)
    connection.iwconfig.return_value = o_e
    print str(iwconfig)
