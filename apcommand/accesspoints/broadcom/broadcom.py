
# python standard library
import time

# this package
from apcommand.baseclass import BaseClass
import apcommand.connections.httpconnection as httpconnection

from apcommand.accesspoints.broadcom.commons import BroadcomRadioData
from apcommand.accesspoints.broadcom.commons import BandEnumeration
from apcommand.accesspoints.broadcom.commons import SSID, SSID_PAGE
from apcommand.accesspoints.broadcom.commons import set_24_data, set_5_data, ssid_page
from apcommand.accesspoints.broadcom.querier import BroadcomRadioQuerier, BroadcomSSIDQuerier
from apcommand.accesspoints.broadcom.querier import BroadcomLANQuerier
from apcommand.accesspoints.broadcom.firmware import BroadcomFirmwareQuerier
from apcommand.accesspoints.broadcom.macros import ChannelChanger

# for some reason Pweave sometimes accepts relative paths, sometimes not
from apcommand.accesspoints.broadcom.commands import DisableInterface
from apcommand.accesspoints.broadcom.commands import EnableInterface

BAND_STRING = '{0} GHz:'
CHANNEL_STRING = '\tChannel: {0}'
SSID_STRING = '\tSSID: {0}'
STATE_STRING = '\tState: {0}'
SIDEBAND_STRING = '\tSideband: {0}'
DHCP_STRING = 'DHCP: {0}'
BOOTLOADER_STRING = 'Bootloader Version: {0}'
OS_STRING = 'OS Version: {0}'
WL_DRIVER_STRING = 'WL Driver Version: {0}'

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
        self._disable_command = None

        # aggregated classes
        self._channel_changer = None
        self._query = None
        self._ssid_query = None
        self._lan_query = None
        self._firmware_query = None
        return

    @property
    def firmware_query(self):
        """
        A BroadcomFirmwareQuery
        """
        if self._firmware_query is None:
            self._firmware_query = BroadcomFirmwareQuerier(connection=self.connection)
        return self._firmware_query


    @property
    def lan_query(self):
        """
        A BroadcomLANQuery 
        """
        if self._lan_query is None:
            self._lan_query = BroadcomLANQuerier(connection=self.connection)
        return self._lan_query
    
    @property
    def disable_command(self):
        """
        A command to disable a wireless interface
        """
        if self._disable_command is None:
            self._disable_command = DisableInterface(connection=self.connection)
        return self._disable_command

    @property
    def enable_command(self):
        """
        a commanad to enable a wireless interface
        """
        if self._enable_command is None:
            self._enable_command = EnableInterface(connection=self.connection)
        return self._enable_command

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
            self._query = {'2':BroadcomRadioQuerier(connection=self.connection,
                                                    band='2.4'),
                             '5':BroadcomRadioQuerier(connection=self.connection,
                                                      band='5')}
        return self._query

    @property
    def ssid_query(self):
        """
        A Broadcom SSID Querier band:reader dictionary
        """
        if self._ssid_query is None:
            self._ssid_query = {'2':BroadcomSSIDQuerier(connection=self.connection,
                                                    band='5'),
                                                    '5':BroadcomSSIDQuerier(connection=self.connection,
                                                      band='2.4')}
        return self._ssid_query

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
        return self.ssid_query[band[0]].ssid

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

    def print_and_log(self, string):
        """
        Sends the string to stdout and the logger (debug)
        """
        print(string)
        self.logger.debug(string)
        return
    
    def get_status(self, band):
        """
        Outputs and logs the status of the AP

        :param:

         - `band`: '2.4', '5', or 'both'

        :postcondition: status strings sent to stdout and logged
        """
        if band is not BandEnumeration.both:
            self.log_status(band)
        else:
            bands = (BandEnumeration.two_point_four, BandEnumeration.five)
            for band in bands:
                self.log_status(band)
        print()
        self.print_and_log(DHCP_STRING.format(self.lan_query.dhcp_state))
        self.print_and_log(BOOTLOADER_STRING.format(self.firmware_query.bootloader_version))
        self.print_and_log(OS_STRING.format(self.firmware_query.os_version))
        self.print_and_log(WL_DRIVER_STRING.format(self.firmware_query.wl_driver_version))
        return

    def log_status(self, band):
        """
        Prints and logs the status for a single band
        """
        self.print_and_log(BAND_STRING.format(band))
        self.print_and_log(CHANNEL_STRING.format(self.get_channel(band)))            
        self.print_and_log(SSID_STRING.format(self.get_ssid(band)))
        self.print_and_log(STATE_STRING.format(self.query[band[0]].state))
        if band.startswith('5'):
            self.print_and_log(SIDEBAND_STRING.format(self.query[band[0]].sideband))
        return

    def unset_channel(self):
        """
        calls an undo.
        """
        self.channel_changer.undo()
        return

    def disable(self, band):
        """
        Sets the disable command's band and calls it.

        :param:

         - `band`: a wireless band (2.4 or 5)
        """
        self.disable_command.band = band
        self.disable_command()
        return

    def enable(self, band):
        """
        Sets the enable command's band and calls it

        :param:

         - `band`: The band of the interface to enable
        """
        self.enable_command.band = band
        self.enable_command()
        return
# end Class BroadcomBCM94718NR