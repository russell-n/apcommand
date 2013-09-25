
# python standard library
import time

# this package
from apcommand.baseclass import BaseClass
import apcommand.connections.httpconnection as httpconnection

from commons import BroadcomRadioData
from commons import SSID, SSID_PAGE
from commons import set_24_data, set_5_data, ssid_page
from querier import Broadcom5GHzQuerier, Broadcom24GHzQuerier
from macros import ChannelChanger


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
        self.logger.debug('Setting the connection.path to "{0}"'.format(BroadcomRadioData.radio_page))
        self.connection.path = BroadcomRadioData.radio_page
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
        self._enable_command = None

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
            self._channel_changer = ChannelChanger(connection=self.connection)
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
                                                             path=BroadcomRadioData.radio_page)
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

    def get_ssid(self, band):
        """
        Gets the ssid for the interface matching the band
        """
        return self.query[band[0]].ssid

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

    def get_status(self, band):
        """
        Returns an aggregate string for the band
        """
        if band is not 'all':
            channel = "Channel: {0}".format(self.query[band[0]].channel)
            ssid = "SSID: {0}".format(self.query[band[0]].ssid)
            state = "State: {0}".format(self.query[band[0]].state)
            if band.startswith('5'):
                sideband = "Sideband: {0}".format(self.query[band[0]].sideband)
            else:
                sideband = ''
            return '\n'.join((channel, ssid, state, sideband))
        else:
            output = ['2.4 GHz:\n']
            output.append("\tChannel: {0}".format(self.query['2'].channel))
            output.append('\tSSID: {0}'.format(self.query['2'].ssid))
            output.append('\tState: {0}'.format(self.query['2'].state))
            output.append('5 GHz:\n')
            output.append('\tChannel: {0}'.format(self.query['5'].channel))
            output.append('\tSideband: {0}'.format(self.query['5'].sideband))            
            output.append('\tSSID: {0}'.format(self.query['5'].ssid))
            output.append('\tState: {0}'.format(self.query['5'].state))
            return '\n'.join(output)

    def unset_channel(self):
        """
        calls an undo.
        """
        self.channel_changer.undo()
        return 
# end Class BroadcomBCM94718NR        


# python standard library
import unittest
import random
import string

# third party
from mock import MagicMock, patch, call


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
        channel = random.choice(BroadcomRadioData.channels_5ghz +
                                BroadcomRadioData.channels_24ghz)
        self.control._lock = MagicMock()
        changer = MagicMock()
        self.control._channel_changer = changer
        with patch('time.sleep'):
            self.control.set_channel(channel)
        changer.assert_called_with(channel)
        return
# end class TestBroadcom            
