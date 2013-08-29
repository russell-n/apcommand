
#python standard libraries
import re
import os

# this package
from apcommand.baseclass import BaseClass
from apcommand.commons.errors import ConfigurationError


class IfconfigError(ConfigurationError):
    """
    raise this if there is a user error
    """
# end class Ifconfig error


class IfconfigCommand(BaseClass):
    """
    The IfconfigCommand interprets ifconfig
    """
    def __init__(self, connection, interface, operating_system=None):
        """
        :param:

         - `connection`: A connection to the device
         - `interface`: The interface to check
         - `operating_system` : The operating system on the devices.
        """
        super(IfconfigCommand, self).__init__()
        self.connection = connection
        self.interface = interface
        self._operating_system = operating_system
        self._ip_address = None
        self._mac_address = None
        self._output = None
        self._ip_expression = None
        return

    @property
    def operating_system(self):
        """
        :return: the operating system for the device to query
        """
        if self._operating_system is None:
            self._operating_system = self.connection.os
        return self._operating_system

    @property
    def ip_address(self):
        """
        :return: The IP Address of the interface 
        """
        return self._match(self.ip_expression,
                           expressions.IP_ADDRESS_NAME)

    @property
    def ip_expression(self):
        """
        :return: a compiled expression to get the ip address
        """
        if self._ip_expression is None:
            if self.operating_system == enumerations.OperatingSystem.linux:
                expression = expressions.LINUX_IP
            elif self.operating_system == enumerations.OperatingSystem.android:
                expression = expressions.ANDROID_IP
            self._ip_expression = re.compile(expression)
        return self._ip_expression
    
    @property
    def mac_address(self):
        """
        :return: MAC Address of the interface
        """
        if self._mac_address is None:
            if self.operating_system == enumerations.OperatingSystem.linux:
                expression = expressions.LINUX_MAC
            elif self.operating_system == enumerations.OperatingSystem.android:
                self._mac_address =  MAC_UNAVAILABLE
                return self._mac_address
            self._mac_address = self._match(re.compile(expression),
                                            expressions.MAC_ADDRESS_NAME)
        return self._mac_address
    
    @property
    def output(self):
        """
        :return: The output of the ifconfig command on the device
        """
        return  self.connection.ifconfig(self.interface)

    def _match(self, expression, name):
        """
        :param:

         - `expression`: The regular expression to match
         - `name`: The group name to pull the match out of the line
         
        :return: The named-group that matched or None
        """
        for line in self.output.output:
            match = expression.search(line)
            if match:
                return match.group(name)
        for line in self.output.error:
            self.logger.error(line)
        return
# end class IfconfigCommand


class IfconfigLexer(BaseClass):
    """
    A class to tokenize ifconfig output
    """
    def __init__(self):
        super(IfconfigLexer, self).__init__()
        self._lines = None
        self._mac_address = None
        return

    @property
    def mac_address(self):
        """
        The Mac address for the interface (assumes only one given)

        :return: the MAC address
        """
        if self._mac_address is None:
            pass
        return self._mac_address


# python standard library
import unittest


sample_output='''
eth0      Link encap:Ethernet  HWaddr 00:14:d1:20:13:a0
          inet addr:192.168.20.50  Bcast:192.168.20.255  Mask:255.255.255.0
          inet6 addr: fe80::214:d1ff:fe20:13a0/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:122979 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8113 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:15636497 (15.6 MB)  TX bytes:1243042 (1.2 MB)
'''.split('\n')
SAMPLE_MAC = '00:14:d1:20:13:a0'
sample_no_ip='''
eth0      Link encap:Ethernet  HWaddr 00:14:d1:20:13:a0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:122979 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8113 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:15636497 (15.6 MB)  TX bytes:1243042 (1.2 MB)
'''.split('\n')



class TestIfconfigLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = IfconfigLexer()
        return

    def test_mac(self):
        """
        Does it get the mac address correctly?
        """
        self.lexer.lines = sample_output
        self.assertEqual(SAMPLE_MAC, self.lexer.mac_address)        
        return
