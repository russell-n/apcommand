
# a decorator to set the page 
def set_page(method):
    """
    Decorator: sets connection.path to self.asp_page before, sleeps after 
    """
    def _method(self, *args, **kwargs):
        if not self.refresh and self.current_page == self.asp_page:
            debug_message = ('Skipping this method (refresh={0},'
                             'current_page={1})').format(self.refresh,
                                                         self.current_page)
            self.logger.debug(debug_message)
            return _method

        self.logger.debug('Setting current_page to {0}'.format(self.asp_page))
        self.current_page = self.asp_page

        self.logger.debug("Setting connection.path to '{0}'".format(self.asp_page))
        self.connection.path = self.asp_page
        outcome = method(self, *args, **kwargs)
        return outcome
    return _method


# python standard library
from abc import ABCMeta, abstractproperty

# this package
from apcommand.baseclass import BaseClass
from commons import BroadcomWirelessData
from commons import BroadcomPages
from commons import BroadcomRadioData
from commons import BroadcomLANData
from commons import BAND_INTERFACE_MAP
from apcommand.accesspoints.broadcom.parser import BroadcomRadioSoup
from apcommand.accesspoints.broadcom.parser import BroadcomSSIDSoup


class BroadcomBaseQuerier(BaseClass):
    """
    A querier for the Broadcom
    """
    __metaclass__ = ABCMeta
    def __init__(self, connection, refresh=False):
        """
        BroadcomBaseQuerier Constructor

        :param:

         - `connection`: Connection to the Broadcom AP
         - `refresh`: if True, call the page even if already loaded
        """
        super(BroadcomBaseQuerier, self).__init__()
        self._logger = None
        self.connection = connection
        self.refresh = refresh
        self.current_page = None
        self._soup = None
        self._asp_page = None
        self._data = None
        return

    @property
    def data(self):
        """
        Data to give the connection (used to specify an interface if needed)

        :default: None
        """
        return None

    @abstractproperty
    def asp_page(self):
        return

    @abstractproperty
    def soup(self):
        """
        A Broadcom Soup to parse the html
        """
        return
        
    @set_page
    def set_soup(self):
        """
        Sets the soup.html to the page specified by self.page

        :precondition:

         - `self.soup` set to correct asp page
         - `self.data` set to dict if needed

        :postcondition: self.soup's html set to text from connection
        """
        text = self.connection(data=self.data).text
        self.soup.html = text        
        return
# end class BroadcomBaseQuerier


class BroadcomRadioQuerier(BroadcomBaseQuerier):
    """
    An aggregator for the two band-queriers    
    """
    def __init__(self, band=None, *args, **kwargs):
        """
        BroadcomQuerier constructor

        :param:

         - `connection`: HTTPConnection to the AP
         - `refresh`: if True, load the html on each call
         - `band`: 2.4 or 5 (this has to be set before using or it will crash)
        """
        super(BroadcomRadioQuerier, self).__init__(*args, **kwargs)
        self._band = None
        self.band = band
        self._mac_address = None
        return

    @property
    def soup(self):
        """
        A BroadcomRadioSoup
        """
        if self._soup is None:
            self._soup = BroadcomRadioSoup()
        return self._soup

    @property
    def data(self):
        """
        the data to tell the connection to choose an interface

        :precondition: self.band is set to valid wireless_interface setting
        """
        if self._data is None:
            self._data = {BroadcomWirelessData.wireless_interface:self.band}
        return self._data

    @property
    def asp_page(self):
        """
        radio.asp
        """
        if self._asp_page is None:
            self._asp_page = BroadcomPages.radio
        return self._asp_page

    @property
    def band(self):
        """
        The band for the chosen interface (2.4 or 5)
        """
        return self._band

    @band.setter
    def band(self, new_band):
        """
        Sets the band (using BAND_INTERFAC_MAP), resets the data (which uses the band)
        """
        if new_band is not None:
            self._band = BAND_INTERFACE_MAP[str(new_band)]
        self._data = None
        return

    @property
    def sideband(self):
        """
        The sideband setting (Upper or Lower), empty for 2.4 GHz
        """
        self.set_soup()
        return self.soup.sideband
    
    @property
    def channel(self):
        """
        Get the current channel for the band
        """
        self.set_soup()
        return self.soup.channel

    @property
    def state(self):
        """
        Get the interface state

        :return: ``Disabled`` or ``Enabled``
        """
        self.set_soup()
        return self.soup.interface_state

    @property
    def mac_address(self):
        """
        Gets the mac-address for this band
        """
        self.set_soup()
        if self.band == BroadcomWirelessData.interface_24_ghz:
            return self.soup.mac_24_ghz        
        elif self.band == BroadcomWirelessData.interface_5_ghz:
            return self.soup.mac_5_ghz
# end class BroadcomRadioQuerier            


class BroadcomSSIDQuerier(BroadcomBaseQuerier):
    """
    A querier for the ssid.asp page
    """
    def __init__(self, band=None, *args, **kwargs):
        super(BroadcomSSIDQuerier, self).__init__(*args, **kwargs)
        self._band = band
        self.band = band
        self._ssid = None
        return

    @property
    def soup(self):
        """
        A BroadcomSSIDSoup
        """
        if self._soup is None:
            self._soup = BroadcomSSIDSoup()
        return self._soup

    @property
    def data(self):
        """
        the data to tell the connection to choose an interface

        :precondition: self.band is set to valid wireless_interface setting
        """
        if self._data is None:
            self._data = {BroadcomWirelessData.wireless_interface:self.band}
        return self._data

    @property
    def asp_page(self):
        """
        ssid.asp
        """
        if self._asp_page is None:
            self._asp_page = BroadcomPages.ssid
        return self._asp_page

    @property
    def band(self):
        """
        The band for the chosen interface (2.4 or 5)
        """
        return self._band

    @band.setter
    def band(self, new_band):
        """
        Sets the band (using BAND_INTERFAC_MAP), resets the data (which uses the band)
        """
        if new_band is not None:
            self._band = BAND_INTERFACE_MAP[str(new_band)]
        self._data = None
        return

    @property
    def ssid(self):
        """
        Get the interface SSID

        :return: 
        """
        self.set_soup()
        return self.soup.ssid
# class BroadcomSSIDQuerier


# python standard library
import unittest

# third-party
from mock import MagicMock, patch, call


TEST_SSID = 'hownowbrowndog'
SSID_ASP = 'ssid_asp.html'


class TestBroadcomQueriers(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.html = MagicMock()
        self.connection.return_value = self.html
        self.html.text = open('radio_5_asp.html').read()
        self.sleep = MagicMock()
        self.querier = BroadcomRadioQuerier(connection=self.connection, band='5')

        # without the patch the calls will sleep and this will take longer
        self.patcher = patch('time.sleep')
        self.mock_sleep = self.patcher.start()
        return

    def tearDown(self):
        self.patcher.stop()
        return

    def test_5_ghz(self):
        """
        Is the band set-up correctly?
        """
        self.querier.band = '5'
        self.assertEqual('1', self.querier.band)
        return

    def test_24_ghz(self):
        """
        Does it set the band correctly?
        """
        self.querier.band = '2.4'
        self.assertEqual('0', self.querier.band)
        return

    def test_sideband(self):
        """
        Does the 5ghz querier get the sideband for you?
        """
        sideband = self.querier.sideband
        self.assertEqual('Lower', sideband)
        return
    
    def test_channel(self):
        """
        Does it get the channel correctily?
        """
        channel =  self.querier.channel
        self.connection.assert_called_with(data={'wl_unit':'1'})
        self.assertEqual(channel, '44')
        return

    def test_state(self):
        """
        Does it get the interface state?
        """
        state = self.querier.state
        self.connection.assert_called_with(data={'wl_unit':'1'})
        self.assertEqual('Enabled', state)
        return

    def test_24_mac_address(self):
        """
        Does it get the MAC address for the 2.4 GHz interface?
        """
        self.querier.band = '2.4'
        mac = self.querier.mac_address
        self.assertEqual('(00:90:4C:09:11:03)', mac)
        return

    def test_5_mac_address(self):
        """
        Does it get the MAC address for the 5 GHz interface?
        """
        mac = self.querier.mac_address
        self.assertEqual('(00:90:4C:13:11:03)', mac)
        return

    def test_5_ssid(self):
        """
        Does it get the right SSID?
        """
        self.html.text = open(SSID_ASP).read()
        querier = BroadcomSSIDQuerier(connection=self.connection,
                                      band='5')
        ssid = querier.ssid
        self.assertEqual(TEST_SSID, ssid)
        return

    def test_no_refresh(self):
        """
        If `refresh` is False, does it not call the radio page twice?
        """
        self.html.text = open(SSID_ASP).read()
        querier = BroadcomSSIDQuerier(connection=self.connection, refresh=False, band='5')
        ssid_1 = querier.ssid
        ssid_2 = querier.ssid
        self.assertEqual([TEST_SSID, TEST_SSID], [ssid_1, ssid_2])
        calls = [call(data={'wl_unit':'1'})]
        self.assertEqual(calls, self.connection.mock_calls)
        return
            
# end class TestBroadcomBaseQuerier    
