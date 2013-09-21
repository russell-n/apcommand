
# python standard library
import time


ZERO = '0'
ONE = '1'

RADIO_OFF, RADIO_ON = ZERO, ONE
RADIO_PAGE = 'radio.asp'
SSID_PAGE = 'ssid.asp'

INTERFACE = 'wl_radio'
CONTROL_CHANNEL = 'wl_channel'
SIDEBAND = 'wl_nctrlsb'
CHANNELS_5GHZ = '36 44 149 157'.split()
CHANNELS_24GHZ = [str(channel) for channel in xrange(1,12)]
SSID = 'wl_ssid'


class BroadcomWirelessData(object):
    """
    A holder of data for the `Wireless Interface`
    """
    __slots__ = ()
    wireless_interface = 'wl_unit'
    interface_5_ghz = ONE
    interface_24_ghz = ZERO


# a decorator to set the page to 'radio.asp'
def radio_page(method):
    """
    Decorator: sets connection.path to radio.asp before, sleeps after
    """
    def _method(self, *args, **kwargs):
        self.logger.debug("Setting connection.path to '{0}'".format(RADIO_PAGE))
        self.connection.path = RADIO_PAGE
        outcome = method(self, *args, **kwargs)
        return outcome
    return _method

# a decorator to set the page to 'ssid.asp'
def ssid_page(method):
    """
    Decorator: sets connection.path to ssid.page before, sleeps after
    """
    def _method(self, *args, **kwargs):
        self.logger.debug("Setting connection.path to {0}".format(SSID_PAGE))
        self.connection.path = SSID_PAGE
        outcome = method(self, *args, **kwargs)
        return outcome
    return _method


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
