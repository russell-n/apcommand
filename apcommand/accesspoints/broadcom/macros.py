
# this package
from apcommand.baseclass import BaseClass
from apcommand.accesspoints.broadcom.commons import BroadcomRadioData
from apcommand.accesspoints.broadcom.commands import DisableInterface, EnableInterface
from apcommand.accesspoints.broadcom.commands import SetChannel, SetSideband
from apcommand.accesspoints.broadcom.commons import BroadcomError


class ChannelChanger(BaseClass):
    """
    A channel changer for the broadcom 
    """
    def __init__(self, connection):
        """
        ChannelChanger constructor

        :param:

         - `connection`: connection to the AP 
        """
        super(ChannelChanger, self).__init__()
        self.connection = connection

        self._enable_command = None
        self._disable_command = None
        self._set_channel_command = None
        self._set_sideband_command = None
        return

    @property
    def enable_command(self):
        """
        An EnableInterface command (without the band set)
        """
        if self._enable_command is None:
            self._enable_command = EnableInterface(connection=self.connection)
        return self._enable_command

    @property
    def disable_command(self):
        """
        A DisableInterface command (without the band set)
        """
        if self._disable_command is None:
            self._disable_command = DisableInterface(connection=self.connection)
        return self._disable_command

    @property
    def set_channel_command(self):
        """
        A SetChannel command
        """
        if self._set_channel_command is None:
            self._set_channel_command = SetChannel(connection=self.connection)
        return self._set_channel_command

    @property
    def set_sideband_command(self):
        """
        A SetSideband command (defaulted 'lower')
        """
        if self._set_sideband_command is None:
            self._set_sideband_command = SetSideband(connection=self.connection)
        return self._set_sideband_command
    
    def undo(self):
        """
        right now just undoes the channel as disable/enable might be called elsewhere
        """
        self.set_channel_command.undo()
        return
        
    def __call__(self, channel):
        """
        The main interface -- enables the Wireless interface and sets the channel

        *Also disables the other wireless interface*

        :param:

         - `channel`: wifi channel to set on the AP
        """
        channel = str(channel)
        with self.connection.lock:
            if channel in BroadcomRadioData.channels_24ghz:
                this_band, other_band = '2.4', '5'

                # disable the other interface
                self.disable_command.band = other_band
                self.disable_command()
                self.logger.debug('Setting 2.4 Ghz Channel ({0})'.format(channel))
                ## now set this interface settings
                self.enable_command.band = this_band
                self.set_channel_command.channel = channel
                
                ## aggregate the settings
                self._set_channel_command += self._enable_command
                
            elif channel in BroadcomRadioData.channels_5ghz:
                band, other_band = '5', '2.4'
                self.logger.debug('Setting 5 GHz Channel ({0})'.format(channel))
                self.logger.debug('Disabling {0}'.format(other_band))
                self.disable_command.band = other_band
                self.logger.debug("Disable Data: {0}".format(self.disable_command.data))
                self.disable_command()

                self.enable_command.band = band
                self.set_channel_command.channel=channel
                self.set_sideband_command.direction = 'lower'
                self._set_channel_command += self._enable_command
                self._set_channel_command += self._set_sideband_command
            else:
                self.logger.error("Valid 5 GHz Channels: {0}".format(','.join(BroadcomRadioData.channels_5ghz)))
                self.logger.error("Valid 2.4 GHz Channels: {0}".format(','.join(BroadcomRadioData.channels_24ghz)))                
                raise BroadcomError("Unknown Channel: {0}".format(channel))
            self.set_channel_command()
            #channel_prime = self.reader(band)
            #if channel_prime != channel:
            #    raise BroadcomError("Channel set failure (expected:{0} actual:{1})".format(channel,
            #                                                                               channel_prime))
        return

# end class BroadcomChannelChanger


# python standard library
import unittest

# third-party
from mock import MagicMock, patch


class TestBroadcomChannelChanger(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.command = ChannelChanger(connection=self.connection)
        self.disable = MagicMock(name='DisableInterface')

        self.disable_patcher = patch('apcommand.accesspoints.broadcom.commands.DisableInterface',
                                     self.disable)
        self.patchers = [self.disable_patcher]
        self.mock_disable = self.disable_patcher.start()
        return

    def tearDown(self):
        for patcher in self.patchers:
            patcher.stop()

    def test_call(self):
        """
        Does it call the right sequence?
        """
        #channel = random.choice(xrange(1,12))
        #self.command(channel)
        #self.disable.assert_called_with()
        return
