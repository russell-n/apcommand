
#python standard library
import re
# this package
from apcommand.baseclass import BaseClass
from apcommand.commons import oatbran


class IwlistEnum(object):
    __slots__ = ()
    channel = 'channel'
    frequency = 'frequency'
# end class IwlistEnum    


class IwlistLexer(BaseClass):
    def __init__(self, interface='wlan0', not_available='NA'):
        """
        IwlistLexer constructor

        :param:

         - `interface`: name of the wifi interface
         - `not_available`: string to return if token not found
        """
        self.interface = interface
        self.not_available = not_available
        self._frequency_expression = None
        self._channel_expression = None        
        return
        
    @property
    def channel_expression(self):
        """
        A compiled regular expression to match the current channel
        """
        if self._channel_expression is None:
            self._channel_expression = re.compile("\(Channel" + oatbran.SPACES  +
                                                    oatbran.NAMED(n=IwlistEnum.channel,
                                                                  e=oatbran.NATURAL) + '\)')
        return self._channel_expression

    def channel(self, lines):
        """
        Gets the current channel

        :param:

         - `lines`: an iterable collection of strings of output from iwlist
        
        :return: string with current channel or not_available if not found
        """        
        return self.search(lines=lines,
                           expression=self.channel_expression,
                           name=IwlistEnum.channel)


    @property
    def frequency_expression(self):
        """
        A compiled regular expression to match the current frequency
        """
        if self._frequency_expression is None:
            self._frequency_expression = re.compile("Current Frequency" + oatbran.OPTIONAL_SPACES + r'(:|=)' +
                                                    oatbran.OPTIONAL_SPACES + 
                                                    oatbran.NAMED(n=IwlistEnum.frequency,
                                                                  e=oatbran.REAL) + oatbran.SPACES + 'GHz')
        return self._frequency_expression

    def frequency(self, lines):
        """
        Gets the current frequency

        :param:

         - `lines`: an iterable collection of strings of output from iwlist
        
        :return: string with current frequency (no units) or not_available if not found
        """        
        return self.search(lines=lines,
                           expression=self.frequency_expression,
                           name=IwlistEnum.frequency)

    def search(self, lines, expression, name):
        """
        Traverses lines and returns named match if expression is matched

        :return: matching sub-string or not_avalable
        """ 
        for line in lines:
            match = expression.search(line)
            if match:
                return match.groupdict()[name]
        return self.not_available



# python standard library
import unittest


sample_output = '''
ath0      47 channels in total; available frequencies :
          Channel 01 : 2.412 GHz
          Channel 02 : 2.417 GHz
          Channel 03 : 2.422 GHz
          Channel 04 : 2.427 GHz
          Channel 05 : 2.432 GHz
          Channel 06 : 2.437 GHz
          Channel 07 : 2.442 GHz
          Channel 08 : 2.447 GHz
          Channel 09 : 2.452 GHz
          Channel 10 : 2.457 GHz
          Channel 11 : 2.462 GHz
          Current Frequency:2.437 GHz (Channel 6)
'''.split('\n')
SAMPLE_FREQUENCY = '2.437'
SAMPLE_CHANNEL = '6'


class TestIwlist(unittest.TestCase):
    def setUp(self):
        self.interface = 'ath0'
        self.iwlist = IwlistLexer(interface=self.interface)
        return
    
    def test_constructor(self):
        """
        Does the constructor take the expected arguments?
        """
        self.assertEqual(self.interface, self.iwlist.interface)
        return

    def test_frequency_expression(self):
        """
        Does the expression math the current frequency?
        """
        sample = "Current Frequency:2.437 GHz (Channel 6)"
        self.assertRegexpMatches(sample, self.iwlist.frequency_expression)
        return

    def test_frequency(self):
        """
        Does the lexer return the frequency string?
        """
        frequency = self.iwlist.frequency(sample_output)
        self.assertEqual(SAMPLE_FREQUENCY, frequency)
        return

    def test_channel_expression(self):
        """
        Does the expression match the channel string?
        """
        sample = "Current Frequency:2.437 GHz (Channel 6)"
        self.assertRegexpMatches(sample, self.iwlist.channel_expression)
        return

    def test_channel(self):
        """
        Does the lexer return the channel?
        """
        channel = self.iwlist.channel(sample_output)
        self.assertEqual(SAMPLE_CHANNEL, channel)
        return
