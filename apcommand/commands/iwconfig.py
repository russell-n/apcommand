"""
A module to extract information from iwconfig
"""
#python standard library
import re
import os

#third-party
from apetools.parsers import oatbran
from apetools.commons.errors import CommandError

class IwconfigEnums(object):
    __slots__ = ()
    ssid = "ssid"
    bssid = "bssid"
    rssi = "rssi"
    noise = 'noise'
    bitrate = 'bitrate'
# end class IwconfigEnums

    
class Iwconfig(object):
    """
    A class to extract `iwconfig` information
    """
    def __init__(self, connection, interface="wlan0", not_available="NA"):
        """
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
        return

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
# end class Iwconfig
