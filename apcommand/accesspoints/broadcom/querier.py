
# python standard library
from abc import ABCMeta, abstractproperty

# this package
from apcommand.baseclass import BaseClass
from commons import BroadcomWirelessData
from commons import BroadcomRadioData
from commons import BroadcomLANData
from commons import SSID_PAGE
from apcommand.accesspoints.broadcom.parser import BroadcomRadioSoup


class PageEnumeration(object):
    __slots__ = ()
    radio = "radio"
    ssid = 'ssid'
    lan = 'lan'


# a decorator to set the page to 'radio.asp'
def radio_page(method):
    """
    Decorator: sets connection.path to radio.asp before, sleeps after 
    """
    def _method(self, *args, **kwargs):
        enumeration = PageEnumeration.radio
        if not self.refresh and self.current_page == enumeration:
            debug_message = ('Skipping this method (refresh={0},'
                             'current_page={1})').format(self.refresh,
                                                         self.current_page)
            self.logger.debug(debug_message)
            return _method

        self.logger.debug('Setting current_page to {0}'.format(enumeration))
        self.current_page = enumeration

        self.logger.debug("Setting connection.path to '{0}'".format(BroadcomRadioData.radio_page))
        self.connection.path = BroadcomRadioData.radio_page
        outcome = method(self, *args, **kwargs)
        return outcome
    return _method

# a decorator to set the page to 'ssid.asp'
def ssid_page(method):
    """
    Decorator: sets connection.path to ssid.page before, sleeps after
    """
    def _method(self, *args, **kwargs):
        enumeration = PageEnumeration.ssid
        if not self.refresh and self.current_page == enumeration:
            debug_message = ('Skipping this method (refresh={0},'
                             'current_page={1})').format(self.refresh,
                                                         self.current_page)
            self.logger.debug(debug_message)
            return _method
        self.logger.debug('Setting current_page to {0}'.format(enumeration))
        self.current_page = enumeration
        self.logger.debug("Setting connection.path to {0}".format(SSID_PAGE))
        self.connection.path = SSID_PAGE
        outcome = method(self, *args, **kwargs)
        return outcome
    return _method

# a decorator to set the page to 'lan.asp'
def lan_page(method):
    """
    Decorator: sets connection.path to lan.asp before, sleeps after 
    """
    def _method(self, *args, **kwargs):
        enumeration = PageEnumeration.lan
        if not self.refresh and self.current_page == enumeration:
            debug_message = ('Skipping this method (refresh={0},'
                             'current_page={1})').format(self.refresh,
                                                         self.current_page)
            self.logger.debug(debug_message)
            return _method

        self.logger.debug('Setting current_page to {0}'.format(enumeration))
        self.current_page = enumeration

        self.logger.debug("Setting connection.path to '{0}'".format(BroadcomLANData.lan_page))
        self.connection.path = BroadcomLANData.lan_page
        outcome = method(self, *args, **kwargs)
        return outcome
    return _method


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
        self._band = None
        self._soup = None
        return

    @abstractproperty
    def band(self):
        """
        Returns the proper setting for the band (UNIT_24_GHZ | UNIT_5_GHZ)
        """
        return

    @abstractproperty
    def mac_address(self):
        """
        Gets the MAC address for this interface
        """
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
    def set_radio_soup(self):
        """
        Sets the soup.html to the radio page
        """
        text = self.connection(data={BroadcomWirelessData.wireless_interface:self.band}).text
        self.soup.html = text        
        return

    @ssid_page
    def set_ssid_soup(self):
        """
        sets soup.html to the ssid page
        """
        text = self.connection(data={BroadcomWirelessData.wireless_interface:self.band}).text
        self.soup.html = text
        return

    @lan_page
    def set_lan_soup(self):
        """
        Sets soup.html to the LAN page
        """
        text = self.connection(data=None).text
        self.soup.html = text
        return
    
    @property
    def sideband(self):
        """
        The sideband setting (Upper or Lower), empty for 2.4 GHz
        """
        self.set_radio_soup()
        return self.soup.sideband
    
    @property
    def channel(self):
        """
        Get the current channel for the band
        """
        self.set_radio_soup()
        return self.soup.channel

    @property
    def state(self):
        """
        Get the interface state

        :return: ``Disabled`` or ``Enabled``
        """
        self.set_radio_soup()
        return self.soup.interface_state

    @property
    def ssid(self):
        """
        Get the interface SSID

        :return: 
        """
        self.set_ssid_soup()
        return self.soup.ssid
# end class BroadcomBaseQuerier


class Broadcom24GHzQuerier(BroadcomBaseQuerier):
    """
    A 24Ghz interface querier
    """
    def __init__(self, *args, **kwargs):
        """
        Broadcom24GHzQuerier constructor
        """
        super(Broadcom24GHzQuerier, self).__init__(*args, **kwargs)
        return

    @property
    def band(self):
        """
        The (Wireless Interface menu) index for 5GHz
        """
        if self._band is None:
            self._band = BroadcomWirelessData.interface_24_ghz
        return self._band

    @property
    def mac_address(self):
        '''
        Gets the mac_address for this interface
        '''
        self.set_radio_soup()
        return self.soup.mac_24_ghz
# end class Broadcom24GHzQuerier


class Broadcom5GHzQuerier(BroadcomBaseQuerier):
    """
    A 5Ghz interface querier
    """
    def __init__(self, *args, **kwargs):
        """
        Broadcom5GHzQuerier constructor
        """
        super(Broadcom5GHzQuerier, self).__init__(*args, **kwargs)
        return

    @property
    def band(self):
        """
        The (Wireless Interface menu) index for 5GHz
        """
        if self._band is None:
            self._band = BroadcomWirelessData.interface_5_ghz
        return self._band

    @property
    def mac_address(self):
        """
        The Mac Address for the 5GHz interface
        """
        self.set_radio_soup()
        return self.soup.mac_5_ghz
# end class Broadcom5GHzQuerier


class BroadcomQuerier(BaseClass):
    """
    An aggregator for the two band-queriers    
    """
    def __init__(self, connection, refresh=False, band=None):
        """
        BroadcomQuerier constructor

        :param:

         - `connection`: HTTPConnection to the AP
         - `refresh`: if True, load the html on each call
         - `band`: 2.4 or 5 (this has to be set before using or it will crash)
        """
        self.connection = connection
        self.refresh = refresh
        self._querier = None
        self._band = band
        return

    @property
    def band(self):
        """
        The wifi band (e.g. 2.4)
        """
        return self._band

    @band.setter
    def band(self, new_band):
        """
        sets the band, resets the querier

        :param:

         - `new_band`: string or number starting with '2' or '5'
        """
        self._band = str(new_band)
        self._querier = None
        return

    @property
    def querier(self):
        """
        A wireless querier
        """
        if self._querier is None:
            if self.band is None:
                raise RuntimeError("BroadcomQuerier.band cannot be None")
            if self.band.startswith('5'):
                self._querier = Broadcom5GHzQuerier(connection=self.connection,
                                                    refresh=self.refresh)
            elif self.band.startswith('2'):
                self._querier = Broadcom24GHzQuerier(connection=self.connection,
                                                     refresh=self.refresh)
        return self._querier

    def __getattr__(self, attribute):
        """
        This is naively pulling the querier properties

        :param:

         - `attribute`: an attribute of the querier (e.g. `channel`)
        """
        return getattr(self.querier, attribute)


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
        self.querier_5 = Broadcom5GHzQuerier(connection=self.connection)
        self.querier_24 = Broadcom24GHzQuerier(connection=self.connection)

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
        self.assertEqual('1', self.querier_5.band)
        return

    def test_24_ghz(self):
        """
        Does it set the band correctly?
        """
        self.assertEqual('0', self.querier_24.band)
        return

    def test_sideband(self):
        """
        Does the 5ghz querier get the sideband for you?
        """
        sideband = self.querier_5.sideband
        self.assertEqual('Lower', sideband)
        return
    
    def test_channel(self):
        """
        Does it get the channel correctily?
        """
        channel =  self.querier_5.channel
        self.connection.assert_called_with(data={'wl_unit':'1'})
        self.assertEqual(channel, '44')
        return

    def test_state(self):
        """
        Does it get the interface state?
        """
        state = self.querier_5.state
        self.connection.assert_called_with(data={'wl_unit':'1'})
        self.assertEqual('Enabled', state)
        return

    def test_24_mac_address(self):
        """
        Does it get the MAC address for the 2.4 GHz interface?
        """
        mac = self.querier_24.mac_address
        self.assertEqual('(00:90:4C:09:11:03)', mac)
        return

    def test_5_mac_address(self):
        """
        Does it get the MAC address for the 5 GHz interface?
        """
        mac = self.querier_5.mac_address
        self.assertEqual('(00:90:4C:13:11:03)', mac)
        return

    def test_5_ssid(self):
        """
        Does it get the right SSID?
        """
        self.html.text = open(SSID_ASP).read()
        ssid = self.querier_5.ssid
        self.assertEqual(TEST_SSID, ssid)
        return

    def test_no_refresh(self):
        """
        If `refresh` is False, does it not call the radio page twice?
        """
        self.html.text = open(SSID_ASP).read()
        querier = Broadcom5GHzQuerier(self.connection, refresh=False)
        ssid_1 = querier.ssid
        ssid_2 = querier.ssid
        self.assertEqual([TEST_SSID, TEST_SSID], [ssid_1, ssid_2])
        calls = [call(data={'wl_unit':'1'})]
        self.assertEqual(calls, self.connection.mock_calls)
        return
            
# end class TestBroadcomBaseQuerier    


class TestBroadcomQuerier(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.html = MagicMock()
        self.connection.return_value = self.html
        self.html.text = open('radio_5_asp.html').read()
        self.sleep = MagicMock()
    
        self.querier = BroadcomQuerier(connection=self.connection)

        # without the patch the calls will sleep and this will take longer
        self.patcher = patch('time.sleep')
        self.mock_sleep = self.patcher.start()
        return

    def tearDown(self):
        self.patcher.stop()
        return


    def test_5_ghz(self):
        """
        Does it use the 5GHz querier if the band is set to 5?
        """
        self.querier.band = '5'
        self.assertEqual('1', self.querier.querier.band)
        return

    def test_24_ghz(self):
        """
        Does it use the 2.4 Ghz querier if the band is set to 2.4?
        """
        self.querier.band = '2'
        self.assertEqual('0', self.querier.querier.band)

        # what if you change?
        self.querier.band = 5
        self.assertEqual('1', self.querier.querier.band)
        return

    def test_mac_address(self):
        """
        Does the getattr work?
        """
        self.querier.band = 5
        mac = self.querier.mac_address
        self.assertEqual('(00:90:4C:13:11:03)', mac)
        return
    
