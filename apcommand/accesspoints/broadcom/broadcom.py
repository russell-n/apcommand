
# python standard library
import time
from abc import ABCMeta, abstractproperty

# this package
from apcommand.baseclass import BaseClass
import apcommand.connections.httpconnection as httpconnection
from apcommand.accesspoints.broadcom.broadcom_parser import BroadcomRadioSoup
from commons import ssid_page, radio_page
from commons import CHANNELS_24GHZ, UNIT_24_GHZ
from commons import CHANNELS_5GHZ, UNIT_5_GHZ
from commons import WIRELESS_INTERFACE, CONTROL_CHANNEL
from commons import RADIO_PAGE, SIDEBAND
from commons import INTERFACE, SSID, SSID_PAGE
from commons import RADIO_ON, RADIO_OFF
from querier import Broadcom5GHzQuerier, Broadcom24GHzQuerier


class BroadcomError(RuntimeError):
    "An Error to raise by broadcom classes"


# a dictionary for data that changes the state of the broadcom
action_dict = lambda: {'action':'Apply'}

def set_24_data():
    """
    return data dictionary to set 2.4 GHz channel
    """
    set_data = action_dict()
    set_data[WIRELESS_INTERFACE] = UNIT_24_GHZ
    return set_data

def set_5_data():
    """
    return data dictionary to set 5 GHz channel
    """
    set_data = action_dict()
    set_data[WIRELESS_INTERFACE] = UNIT_5_GHZ
    return set_data


class RadioPageConnection(BaseClass):
    """
    A context manager for connecting to the radio.asp page
    """
    def __init__(self, connection, sleep=0.5):
        """
        RadioPageConnection constructor

        :param:

         - `connection`: Connection to the broadcom
         - `sleep`: Time to sleep before exiting
        """
        super(RadioPageConnection, self).__init__()
        self.connection = connection
        self.sleep = sleep
        return

    def __enter__(self):
        """
        Sets the path and returns the connection
        """
        self.logger.debug('Setting the connection.path to "{0}"'.format(RADIO_PAGE))
        self.connection.path = RADIO_PAGE
        return self.connection

    def __exit__(self, type, value, traceback):
        self.logger.debug('Sleeping for {0} seconds'.format(self.sleep))
        time.sleep(self.sleep)
        return
# end RadioPageConnection


class BroadcomBCM94718NR(BaseClass):
    """
    A class to control and query the Broadcom BCM94718NR
    """
    def __init__(self, hostname='192.168.1.1', username='',
                 password='admin', sleep=0.1):
        """
        BroadcomBCM94718NR Constructor

        :param:

         - `hostname`: address of the AP
         - `username`: login username (use empty string if none)
         - `password`: login password (use empty string if none)
         - `sleep`: seconds to sleep after a call to the web server
        """
        super(BroadcomBCM94718NR, self).__init__()
        self.hostname = hostname
        self.username = username
        self.password = password
        self.sleep = sleep
        self._connection = None
        self._enable_24_data = None
        self._enable_5_data = None
        self._disable_24_data = None
        self._disable_5_data = None
        self._set_24_data = None
        self._set_5_data = None
        self._set_sideband_lower_data = None        
        self._channel_map = None

        # aggregated classes
        self._channel_changer = None
        self._query = None
        return

    @property
    def channel_changer(self):
        """
        A BroadcomChannelChanger
        """
        if self._channel_changer is None:
            self._channel_changer = BroadcomChannelChanger(connection=self.connection,
                                                           sleep=self.sleep)
        return self._channel_changer

    @property
    def query(self):
        """
        A Broadcom Querier band:reader dictionary
        """
        if self._query is None:
            self._query = {'2':Broadcom24GHzQuerier(connection=self.connection),
                             '5':Broadcom5GHzQuerier(connection=self.connection)}
        return self._query

    @property
    def connection(self):
        """
        A connection to the AP (right now this acts as an HTTPConnection builder)

        :return: HTTPConnection for the DUT (set to radio.asp pgae)
        """
        if self._connection is None:
            self._connection = httpconnection.HTTPConnection(hostname=self.hostname,
                                                             username=self.username,
                                                             password=self.password,
                                                             rest=self.sleep,
                                                             path=RADIO_PAGE)
        return self._connection

    @ssid_page
    def set_5_ssid(self, ssid):
        """
        Sets the 5 Ghz band SSID
        """
        data = set_5_data()
        data[SSID] = ssid
        self.connection(data=data)
        return

    @ssid_page
    def set_24_ssid(self, ssid):
        """
        Sets the 2.4 Ghz band SSID
        """
        data = set_24_data()
        data[SSID] = ssid
        self.connection(data=data)
        return

    def set_channel(self, channel):
        """
        Sets the wifi channel

        :param:

         - `channel`: wifi channel to set
        """
        self.channel_changer(channel)
        return

    def get_channel(self, band):
        """
        Returns the channel for the given band (uses only first character)
        """
        return self.query[band[0]].channel
# end Class BroadcomBCM94718NR        


class BroadcomBaseCommand(BaseClass):
    """
    The base-command to hold the data-dict
    """
    __metaclass__ = ABCMeta
    def __init__(self, connection, sleep=0.5):
        """
        Base Command constructor

        :param:

         - `connection`: Connection to the AP
         - `sleep`: seconds to sleep after talking to the AP
        """
        super(BroadcomBaseCommand, self).__init__()
        self._logger = None
        self.connection = connection
        self.sleep = sleep
        self._base_data = None
        self._query = None
        return

    @abstractproperty
    def base_data(self):
        """
        the data-dictionary without the command-specific data
        """
        return

    @abstractproperty
    def query(self):
        """
        A Broadcom Querier
        """
        return


class Base5GHzCommand(BroadcomBaseCommand):
    """
    A base for 5Ghz commands
    """
    def __init__(self, *args, **kwargs):
        super(Base5GHzCommand, self).__init__(*args, **kwargs)
        self._logger = None
        return

    @property
    def base_data(self):
        """
        The data-dict to set the 5ghz interface
        """
        if self._base_data is None:
            self._base_data = action_dict()
            self._base_data[WIRELESS_INTERFACE] = UNIT_5_GHZ
        return self._base_data

    @property
    def query(self):
        """
        a Broadcom5GHz Querier
        """
        if self._query is None:
            self._query = Broadcom5GHzQuerier(connection=self.connection)            
        return self._query
# end class Base5GHzCommand


class BroadcomChannelChanger(BaseClass):
    """
    A channel changer for the broadcom 
    """
    def __init__(self, connection, sleep=0.5):
        """
        BroadcomChannelChanger constructor

        :param:

         - `connection`: connection to the AP 
         - `sleep`: seconds to sleep between calls
        """
        super(BroadcomChannelChanger, self).__init__()
        self.connection = connection
        self.sleep = sleep
        self._channel_map = None
        self._set_sideband_lower_data = None
        self._enable_24_data = None
        self._disable_5_data = None
        self._disable_24_data = None
        self._enable_5_data = None
        self._reader = None
        return

    @property
    def reader(self):
        """
        A BroadcomChannelReader
        """
        if self._reader is None:
            self._reader = BroadcomChannelReader(connection=self.connection)
        return self._reader

    @property
    def enable_5_data(self):
        """
        The data to send to the connection to enable 5 GHz

        :return: dict of data-values for the connection
        """
        if self._enable_5_data is None:
            self._enable_5_data = action_dict()
            self._enable_5_data['wl_unit'] = UNIT_5_GHZ
            self._enable_5_data['wl_radio'] = RADIO_ON
        return self._enable_5_data

    @property
    def disable_24_data(self):
        """
        Dictionary of data to disable the 2.4GHz interface
        """
        if self._disable_24_data is None:
            self._disable_24_data = action_dict()
            self._disable_24_data[WIRELESS_INTERFACE] = UNIT_24_GHZ
            self._disable_24_data[INTERFACE] = RADIO_OFF
        return self._disable_24_data

    @property
    def disable_5_data(self):
        """
        Data dictionary to disable the 5 Ghz interface
        """
        if self._disable_5_data is None:
            self._disable_5_data = action_dict()
            self._disable_5_data[WIRELESS_INTERFACE] = UNIT_5_GHZ
            self._disable_5_data[INTERFACE] = RADIO_OFF
        return self._disable_5_data        

    @property
    def set_sideband_lower_data(self):
        """
        A data dictionary to set the sideband to Lower
        """
        if self._set_sideband_lower_data is None:
            self._set_sideband_lower_data = action_dict()
            self._set_sideband_lower_data[WIRELESS_INTERFACE] = UNIT_5_GHZ
            self._set_sideband_lower_data[SIDEBAND] = 'lower'
        return self._set_sideband_lower_data

    @property
    def channel_map(self):
        """
        Map of channel to data-dictionary
        """
        if self._channel_map is None:
            channel_24 = [str(channel) for channel in range(1,12)]
            channel_24_data = [set_24_data()] * len(channel_24)
            # these are the only channels that match the Atheros channels we chose
            channel_5 = CHANNELS_5GHZ
            channel_5_data = [set_5_data()] * len(channel_5)
            channels = channel_24 + channel_5
            data = channel_24_data + channel_5_data         
            self._channel_map = dict(zip(channels, data))
        return self._channel_map

    @radio_page
    def disable_24_ghz(self):
        """
        Disables the 2.4Ghz radio
        """
        self.logger.debug("Disabling the 2.4 GHz Radio")
        self.connection(data=self.disable_24_data)
        return

    @radio_page
    def disable_5_ghz(self):
        """
        Disables the 5 GHz radio
        """
        self.logger.debug('Disabling the 5 GHz radio')
        self.connection(data=self.disable_5_data)
        return

    def set_channel(self, channel):
        """
        Sets the channel on the AP (and the sideband if 5ghz) 
        """
        self.logger.debug('Setting the channel to {0}'.format(channel))
        channel = str(channel)
        data = self.channel_map[channel]
        data[CONTROL_CHANNEL] = channel
        # I decided not to use @radio_page because I call set_sideband_lower
        with RadioPageConnection(self.connection, self.sleep):
            self.connection(data=data)

        if channel in CHANNELS_5GHZ:
            self.set_sideband_lower()
        return

    @radio_page
    def set_sideband_lower(self):
        """
        To match the Atheros the 5GHz channels are only set 'lower'
        """
        self.logger.debug("setting the sideband to 'Lower'")
        self.connection(data=self.set_sideband_lower_data)
        return

    @radio_page
    def enable_5_ghz(self):
        """
        Tells the connection to turn on the 5 GHz radio
        """
        self.logger.debug("Enabling the 5 Ghz radio")
        self.connection(data=self.enable_5_data)
        return

    @radio_page
    def enable_24_ghz(self):
        """
        Tells the connection to turn on the 2.4 GHz radio
        """
        self.logger.debug("Enabling the 2.4 GHz radio")
        self.connection(data=self.enable_24_data)
        return

    @property
    def enable_24_data(self):
        """
        The data to send to the connection to enable 2.4 GHz

        :return: dict of data-values for the connection
        """
        if self._enable_24_data is None:
            self._enable_24_data = action_dict()
            self._enable_24_data[WIRELESS_INTERFACE] = UNIT_24_GHZ
            self._enable_24_data[INTERFACE] = RADIO_ON
        return self._enable_24_data

    def __call__(self, channel):
        """
        The main interface -- enables the Wireless interface and sets the channel

        *Also disables the other wireless interface*

        :param:

         - `channel`: wifi channel to set on the AP
        """
        channel = str(channel)
        with self.connection.lock:
            if channel in CHANNELS_24GHZ:
                band = '2.4'
                self.logger.debug('Setting 2.4 Ghz Channel ({0})'.format(channel))                
                self.enable_24_ghz()
                self.disable_5_ghz()
            elif channel in CHANNELS_5GHZ:
                band = '5'
                self.logger.debug('Setting 5 GHz Channel ({0})'.format(channel))
                self.enable_5_ghz()
                self.disable_24_ghz()
            else:
                self.logger.error("Valid 5 GHz Channels: {0}".format(','.join(CHANNELS_5GHZ)))
                self.logger.error("Valid 2.4 GHz Channels: {0}".format(','.join(CHANNELS_24GHZ)))                
                raise BroadcomError("Unknown Channel: {0}".format(channel))
            self.set_channel(channel)
            channel_prime = self.reader(band)
            if channel_prime != channel:
                raise BroadcomError("Channel set failure (expected:{0} actual:{1})".format(channel,
                                                                                           channel_prime))

        return

# end class BroadcomChannelChanger


class BroadcomChannelReader(BaseClass):
    """
    A class to get a channel reading from the broadcom AP
    """
    def __init__(self, connection, sleep=0.5):
        """
        BroadcomChannelReader constructor

        :param:

         - `connection`: Connection to the AP
         - `sleep`: Seconds to sleep after calling the connection
        """
        super(BroadcomChannelReader, self).__init__()
        self.connection = connection
        self.sleep = sleep
        self._soup = None
        return

    @property
    def soup(self):
        """
        A BroadcomRadioSoup to parse the html
        """
        if self._soup is None:
            self._soup = BroadcomRadioSoup()
        return self._soup

    @radio_page
    def __call__(self, band):
        """
        Get the current channel for the band

        :param:

         - `band`: '2.4' or '5' (only checks first character)

        :raise: BroadcomError if band not known
        """
        band = str(band)
        if band.startswith('2'):
            text = self.connection(data={WIRELESS_INTERFACE:UNIT_24_GHZ}).text
            self.soup.html = text
        elif band.startswith('5'):
            text = self.connection(data={WIRELESS_INTERFACE:UNIT_5_GHZ}).text
            self.soup.html = text
        else:
            self.logger.error('Valid Bands: 2.4, 5')
            raise BroadcomError("unrecognized band: {0}".format(band))
        return self.soup.channel
# end class BroadcomChannelReader    


# python standard library
import unittest
import random
import string

# third party
from mock import MagicMock, patch, call
from nose.tools import raises

# this package
from querier import Broadcom5GHzQuerier


EMPTY_STRING = ''
random_letters = lambda: EMPTY_STRING.join([random.choice(string.letters)
                                            for c in xrange(random.randrange(100))])


class TestBroadcomBCM94718NR(unittest.TestCase):
    def setUp(self):
        self.hostname = random_letters()
        self.username = random_letters()
        self.password = random_letters()
        self.connection = MagicMock(name='MockHTTPConnection')
        self.control = BroadcomBCM94718NR(hostname=self.hostname,
                                          username=self.username,
                                          password=self.password)
        self.control._connection = self.connection
        return

    def test_defaults(self):
        """
        Do the defaults match the Broadcom's 'reset' values?
        """
        connection = BroadcomBCM94718NR()
        self.assertEqual('192.168.1.1', connection.hostname)
        self.assertEqual('', connection.username)
        self.assertEqual('admin', connection.password)
        return

    def test_constructor(self):
        """
        Does it construct the control correctly?
        """
        self.assertEqual(self.hostname, self.control.hostname)
        self.assertEqual(self.username, self.control.username)
        self.assertEqual(self.password, self.control.password)
        return

    def test_connection(self):
        """
        Does the control build the HTTPConnection?
        """
        connection = MagicMock(name='HTTPConnection')
        control = BroadcomBCM94718NR()
        with patch('apcommand.connections.httpconnection.HTTPConnection', connection):
            print connection.mock_calls
            print control.connection.mock_calls
            # for some reason this isn't working (the patch is created but not called)
            #control.connection.assert_called_with(hostname='192.168.1.1')
            self.assertIsInstance(control.connection, MagicMock)
        return

    def test_set_ssid(self):
        """
        Does the connection get the right data to set the ssid?
        """
        ssid = random_letters()
        with patch('time.sleep'):
            self.control.set_5_ssid(ssid)
        self.assertEqual(self.connection.path, SSID_PAGE)
        calls = [call(data={'wl_unit':'1', 'wl_ssid':ssid, 'action':'Apply'})]
        self.assertEqual(self.connection.mock_calls, calls)

        with patch('time.sleep'):
            self.control.set_24_ssid(ssid)
        calls += [call(data={'wl_unit':'0', 'wl_ssid':ssid, 'action':'Apply'})]
        self.assertEqual(self.connection.mock_calls, calls)
        return

    def test_set_channel(self):
        """
        Does it call the BroadcomChannelChanger?
        """
        channel = random.choice(CHANNELS_5GHZ + CHANNELS_24GHZ)
        self.control._lock = MagicMock()
        changer = MagicMock()
        self.control._channel_changer = changer
        with patch('time.sleep'):
            self.control.set_channel(channel)
        changer.assert_called_with(channel)
        return
# end class TestBroadcom            


class TestBroadcomChannelChanger(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.lock = MagicMock()
        self.soup = MagicMock()
        self.reader = MagicMock()
        self.connection.lock = self.lock
        self.changer = BroadcomChannelChanger(connection=self.connection)
        self.changer._reader = self.reader
        self.changer.reader.soup = self.soup
        return

    def test_constructor(self):
        """
        Does the signature match expectations?
        """
        self.assertEqual(self.connection, self.changer.connection)    
        return

    def test_set_channel(self):
        """
        Does it send the right channel (and sideband if appropriate)
        """
        channel_24 = str(random.randrange(1,12))
        with patch('time.sleep'):
            self.changer.set_channel(channel_24)
        first_call = [call(data={'wl_unit':'0',
                                'wl_channel':channel_24,
                                'action':'Apply'}) ]
        self.assertEqual(self.connection.mock_calls, first_call)

        channel_5 = random.choice('36 44 149 157'.split())
        with patch('time.sleep'):
            self.changer.set_channel(channel_5)
        calls = first_call + [call(data={'wl_unit':'1','wl_channel': channel_5,'action':'Apply'}),
                 call(data={'wl_unit':'1', 'wl_nctrlsb':'lower', 'action':'Apply'})]
        self.assertEqual(self.connection.mock_calls, calls)
        self.assertEqual(self.connection.path, RADIO_PAGE)
        return

    def test_24_call(self):
        """
        Does it set the enabled interface and channel for 2.4 GHz?
        """
        channel = str(random.randint(1,11))
        self.changer.reader.return_value = channel
        with patch('time.sleep'):
            self.changer(channel)
        calls = [call.lock.__enter__(),
                 call(data={'wl_unit':'0', 'wl_radio':'1', 'action':"Apply"}),
                 call(data={'wl_unit':'1','wl_radio':'0','action':'Apply'}),
                 call(data={'wl_unit':'0','wl_channel':channel,'action':'Apply'}),
                 call.lock.__exit__(None, None, None)]
        self.assertEqual(calls, self.connection.mock_calls)
        self.assertEqual(self.connection.path, RADIO_PAGE)
        self.assertEqual(RADIO_PAGE, self.connection.path )
        return

    @raises(BroadcomError)
    def test_bad_call(self):
        "Does it raise a Broadcom Error if the channel fails to set?"
        reader = MagicMock()
        self.changer._reader = reader
        channel = random.choice(CHANNELS_24GHZ)
        reader.channel = random_letters()
        with patch('time.sleep'):
            self.changer(channel)
        return

    def test_5_call(self):
        """
        Does it set the enabled interface and channel for 5 GHz?
        """
        channel = random.choice(CHANNELS_5GHZ)

        self.changer.reader.return_value = channel

        with patch('time.sleep'):
            self.changer(channel)
        # enable 5, disable 2.4, set channel
        calls = [call.lock.__enter__(),
                 call(data={'wl_unit':'1', 'wl_radio':'1', 'action':'Apply'}),                 
                 call(data={'wl_unit':'0','wl_radio':'0','action':"Apply"}),
                 call(data={'wl_unit':'1','wl_channel': channel,'action':'Apply'}),
                 call(data={'wl_unit':'1', 'wl_nctrlsb':'lower', 'action':'Apply'}),
                 call.lock.__exit__(None, None, None)]
        self.assertEqual(calls, self.connection.mock_calls)
        self.assertEqual(self.connection.path, RADIO_PAGE)

        self.assertEqual(RADIO_PAGE, self.connection.path )
        return

    def test_enable_5_interface(self):
        """
        Does it call the connection with the right data?
        """
        self.connection.path = None
        with patch('time.sleep'):
            self.changer.enable_5_ghz()
        self.connection.assert_called_with(data={'wl_unit':'1', 'wl_radio':'1', 'action':'Apply'})
        self.assertEqual(RADIO_PAGE, self.connection.path)
        return


    def test_disable_5_interface(self):
        """
        Does the connection get the data to disable the 5 GHz data?
        """
        self.connection.path = None
        with patch('time.sleep'):
            self.changer.disable_5_ghz()
        self.connection.assert_called_with(data={'wl_unit':'1',
                                                 'wl_radio':'0',
                                                 'action':'Apply'})
        self.assertEqual(self.connection.path, RADIO_PAGE)
        return

    def test_enable_24_interface(self):
        """
        Does it enable the 2.4 GHz interface?
        """
        self.connection.path = None
        with patch('time.sleep'):
            self.changer.enable_24_ghz()
        self.connection.assert_called_with(data={'wl_unit':'0', 'wl_radio':'1', 'action':"Apply"})
        self.assertEqual(RADIO_PAGE, self.connection.path )
        return

    def test_disable_24_interface(self):
        """
        Is the right data sent to disable the 2.4 GHz interface?
        """
        self.connection.path = None
        with patch('time.sleep'):
            self.changer.disable_24_ghz()
        self.connection.assert_called_with(data={'wl_unit':'0',
                                                 'wl_radio':'0',
                                                 'action':"Apply"})
        self.assertEqual(RADIO_PAGE, self.connection.path)
        return


class TestBroadcomChannelReader(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.lock = MagicMock()
        self.connection.lock = self.lock
        self.soup = MagicMock()
        self.reader = BroadcomChannelReader(connection=self.connection)
        self.reader._soup = self.soup
        return

    def test_constructor(self):
        """
        Does the constructor set the parameters correctly?
        """
        self.assertEqual(self.connection, self.reader.connection)
        return

    def test_call(self):
        """
        Does it execute the correct sequence of calls to get the channel?
        """
        band = '2.4'

        channel = random.choice(CHANNELS_24GHZ)
        self.soup.channel = channel

        with patch('time.sleep'):
            read_value = self.reader(band)
        calls = [call(data={'wl_unit':'0'})]
        self.assertEqual(self.connection.mock_calls, calls)
        self.assertEqual(channel, read_value)

        band = 5
        channel = random.choice(CHANNELS_5GHZ)
        self.soup.channel = channel

        with patch('time.sleep'):
            read_value = self.reader(band)
        calls += [call(data={'wl_unit':'1'})]
        self.assertEqual(self.connection.mock_calls, calls)
        self.assertEqual(channel, read_value)
        return


class BadChild(BroadcomBaseCommand):
    def query(self):
        return

class BadChild2(BroadcomBaseCommand):
    def base_data(self):
        return

class EvilChild(BroadcomBaseCommand):
    def base_data(self):
        return
    def query(self):
        return
    
class TestBroadcomCommands(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        return

    def test_abstract_property(self):
        """
        Does a class without the properties defined crash on creation?
        """
        self.assertRaises(TypeError, BroadcomBaseCommand, args=(self.connection,))
        self.assertRaises(TypeError, BadChild, args=(self.connection,))
        self.assertRaises(TypeError, BadChild2, args=(self.connection,))
        EvilChild(self.connection)
        return

    def test_base_commands(self):
        """
        Do the band-specific base-commands build the right data and queries?
        """
        base_5 = Base5GHzCommand(connection=self.connection)
        data_dict = action_dict()
        data_dict['wl_unit'] = '1'
        self.assertEqual(data_dict, base_5.base_data)
        self.assertEqual(Broadcom5GHzQuerier, type(base_5.query))
        return
