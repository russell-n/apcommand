
# python standard library
import time


ZERO = '0'
ONE = '1'

SSID_PAGE = 'ssid.asp'
SSID = 'wl_ssid'


class BandEnumeration(object):
    __slots__ = ()
    two_point_four = '2.4'
    five = '5'


class BroadcomRadioData(object):
    """
    A holder of constants for setting or checking the channel
    """
    __slots__ = ()
    channels_5ghz =  '36 44 149 157'.split()
    channels_24ghz = [str(channel) for channel in xrange(1,12)]
    radio_page = 'radio.asp'
    interface = 'wl_radio'
    radio_off = ZERO
    radio_on = ONE
    control_channel = 'wl_channel'
    sideband = 'wl_nctrlsb'
# end BroadcomRadioData


class BroadcomLANData(object):
    __slots__ = ()
    lan_page = 'lan.asp'


class BroadcomWirelessData(object):
    """
    A holder of data for the `Wireless Interface`
    """
    __slots__ = ()
    wireless_interface = 'wl_unit'
    interface_5_ghz = ONE
    interface_24_ghz = ZERO


class BroadcomPages(object):
    """
    Holds the names of the web pages
    """
    __slots__ = ()
    radio = 'radio.asp'
    lan = 'lan.asp'
    ssid = 'ssid.asp'
    firmware = 'firmware.asp'
    security = 'security.asp'
    


# a decorator to set the page to 'radio.asp'
def radio_page(method):
    """
    Decorator: sets connection.path to radio.asp before, sleeps after
    """
    def _method(self, *args, **kwargs):
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
        self.logger.debug("Setting connection.path to {0}".format(SSID_PAGE))
        self.connection.path = SSID_PAGE
        outcome = method(self, *args, **kwargs)
        return outcome
    return _method

# a decorator to set the page assuming that the object has a self.asp_page attribute
def set_page(method):
    """
    Decorator: sets connection.path to self.asp_page before, sleeps after
    """
    def _method(self, *args, **kwargs):
        self.logger.debug("Setting connection.path to {0}".format(self.asp_page))
        self.connection.path = self.asp_page
        outcome = method(self, *args, **kwargs)
        return outcome
    return _method



# a dictionary for data that changes the state of the broadcom
action_dict = lambda: {'action':'Apply'}

def set_24_data():
    """
    return data dictionary to set 2.4 GHz channel
    """
    data = BroadcomWirelessData
    set_data = action_dict()
    set_data[data.wireless_interface] = data.interface_24_ghz
    return set_data

def set_5_data():
    """
    return data dictionary to set 5 GHz channel
    """
    data = BroadcomWirelessData
    set_data = action_dict()
    set_data[data.wireless_interface] = data.interface_5_ghz
    return set_data


class BroadcomError(RuntimeError):
    "An Error to raise by broadcom classes"
