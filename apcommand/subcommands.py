
def try_except(func):
    """
    A decorator method to catch Exceptions

    :param:

     - `func`: A function to call
    """
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            import traceback
            log = BaseClass()
            log.logger.error(error)
            log.logger.debug(traceback.format_exc())
    return wrapped


# this package
from apcommand.baseclass import BaseClass
import apcommand.accesspoints.atheros
from apcommand.commons.errors import ArgumentError


class SubCommand(BaseClass):
    """
    A holder of sub-commands
    """
    def __init__(self):
        """
        SubCommand Constructor
        """
        super(SubCommand, self).__init__()
        return

    def access_point(self, args):
        '''
        The Access point controller

        '''
        # assume that the accesspoint class has valuable defaults
        # only pass in parameters that have been set by the arguments
        apargs = ('hostname', 'username', 'password')
        apvalues = (getattr(args, arg) for arg in apargs if getattr(args, arg) is not None)
        apkeys = (arg for arg in apargs if getattr(args, arg) is not None)
        apkwargs = dict(zip(apkeys, apvalues))

        ap = apcommand.accesspoints.atheros.AtherosAR5KAP(**apkwargs)
        return ap

    @try_except
    def up(self, args):
        """
        The AP up sub-command

        :postcondition: ap.up() called
        """
        ap = self.access_point(args)
        ap.up()
        return

    @try_except
    def down(self, args):
        """
        The AP Down sub-command

        :postcondition: ap.down() called on ap from access_point(args)
        """
        ap = self.access_point(args)
        ap.down()
        return
    
    @try_except
    def destroy(self, args):
        """
        Destroys an interface

        :param:

         - `args`: namespace with `interface` attribute
        
        :postcondition: ap.destroy(interface) is called
        """
        ap = self.access_point(args)
        ap.destroy(args.interface)
        return

    @try_except
    def status(self, args):
        """
        Calls the access-point control's status method

        :param:

         - `args`: namespace with 'interface' attribute
        """
        ap = self.access_point(args)
        ap.status(args.interface)
        return

    @try_except
    def reset(self, args):
        """
        Calls the access point's reset method

        :param:

         - `args`: namespace with `interface` attribute
        """
        ap = self.access_point(args)
        ap.reset(args.interface)
        return

    @try_except
    def channel(self, args):
        """
        Calls the access point's set_channel method

        :param:

         - `args`: namespace with `channel` and `mode` attribute
        """
        ap = self.access_point(args)
        ap.set_channel(channel=args.channel,
                       mode=args.mode)
        return

    @try_except
    def ssid(self, args):
        """
        Calls the access point's set_ssid method

        :param:

         - `args`: namespace with `interface` and `ssid` attributes
        """
        ap = self.access_point(args)
        ap.set_ssid(interface=args.interface,
                    ssid=args.ssid)
        return

    @try_except
    def security(self, args):
        """
        calls the AP's set_security method

        :param:

         - `args`: namespace with `type` attribute
        """
        ap = self.access_point(args)
        ap.set_security(type=args.type)
        return


# python standard library
import unittest
# third-party
from mock import MagicMock, patch


class TestSubCommand(unittest.TestCase):
    def setUp(self):
        self.logger = MagicMock()
        self.sub_command = SubCommand()
        self.sub_command._logger = self.logger
        return

    def test_args(self):
        """
        Does the correct set of arguments get passed to the ap
        """
        args = MagicMock()
        del args.channel
        args.hostname = 'mike'
        args.username = 'bob'
        args.password = 'me'
        ap = MagicMock()
        with patch('apcommand.accesspoints.atheros', ap):
            # 000
            access_point = self.sub_command.access_point(args)
            ap.AtherosAR5KAP.assert_called_with(hostname=args.hostname,
                                                username=args.username,
                                                password=args.password)
            args.password = None
            # 001
            access_point = self.sub_command.access_point(args)
            ap.AtherosAR5KAP.assert_called_with(hostname=args.hostname,
                                                username=args.username)
            args.username = None
            # 011
            access_point = self.sub_command.access_point(args)
            ap.AtherosAR5KAP.assert_called_with(hostname=args.hostname)
            
            args.password = 'cow'
            # 010
            access_point = self.sub_command.access_point(args)
            ap.AtherosAR5KAP.assert_called_with(hostname=args.hostname,
                                                password=args.password)
            args.hostname=None
            # 110
            access_point = self.sub_command.access_point(args)
            ap.AtherosAR5KAP.assert_called_with(password=args.password)
            args.password = None
            # 111
            access_point = self.sub_command.access_point(args)
            ap.AtherosAR5KAP.assert_called_with()            
        return
        

    def test_up(self):
        """
        Does it have the up-method and will it catch exception?
        """
        args = MagicMock()
        del args.channel
        self.assertTrue(hasattr(self.sub_command, 'up'))
        ap_up = MagicMock()
        ap_instance = MagicMock()
        ap_up.AtherosAR5KAP.return_value = ap_instance
        error_message = "this is an error"
        ap_instance.up.side_effect = Exception(error_message)
        base = MagicMock()
        with patch('apcommand.accesspoints.atheros', ap_up):
            self.sub_command.up(args)
            ap_instance.up.assert_called_with()
        return

    def test_down(self):
        """
        Does it have the down-method and will it catch exception?
        """
        args = MagicMock()
        del args.channel
        self.assertTrue(hasattr(self.sub_command, 'down'))
        ap_down = MagicMock()
        ap_instance = MagicMock()
        ap_down.AtherosAR5KAP.return_value = ap_instance
        error_message = "this is an error"
        ap_instance.down.side_effect = Exception(error_message)
        with patch('apcommand.accesspoints.atheros', ap_down):
            self.sub_command.down(args)
            ap_instance.down.assert_called_with()
        return

    def test_destroy(self):
        """
        Does it have a method to destroy a (virtual) interface?
        """
        self.assertTrue(hasattr(self.sub_command, 'destroy'))
        args = MagicMock()
        # args.channel has to be deleted or hasattr will return True
        del args.channel
        args.interface = 'ath0'
        ap_destroy = MagicMock()
        ap_instance = MagicMock()
        ap_destroy.AtherosAR5KAP.return_value = ap_instance
        error_message = "this is an error"
        ap_instance.destroy.side_effect = Exception(error_message)
        with patch('apcommand.accesspoints.atheros', ap_destroy):
            self.sub_command.destroy(args)
            ap_instance.destroy.assert_called_with('ath0')
        return

    def test_status(self):
        """
        Does the sub-command call the ap's status method?
        """
        self.assertTrue(hasattr(self.sub_command, 'status'))
        args = MagicMock()
        del args.channel
        args.interface = 'ath0'
        ap_status = MagicMock()
        ap_instance = MagicMock()
        ap_status.AtherosAR5KAP.return_value = ap_instance
        error_message = "this is an error"
        ap_instance.status.side_effect = Exception(error_message)
        with patch('apcommand.accesspoints.atheros', ap_status):
            self.sub_command.status(args)
            ap_instance.status.assert_called_with('ath0')
        return

    def test_channel(self):
        """
        Does the set_channel method get called correctly?
        """
        args = MagicMock()
        args.channel = '1'
        args.mode='11n'
        ap_channel = MagicMock()
        ap_instance = MagicMock()
        ap_channel.AtherosAR5KAP.return_value = ap_instance
        error_message = 'channel setting error'
        ap_instance.set_channel.side_effect = Exception(error_message)
        with patch('apcommand.accesspoints.atheros', ap_channel):
            self.sub_command.channel(args)
            ap_instance.set_channel.assert_called_with(channel=args.channel, mode=args.mode)
        return

    def test_security(self):
        """
        Does the set_security method get called correctly?
        """
        args = MagicMock()
        args.type = 'open'
        ap_module = MagicMock()
        ap_instance = MagicMock(spec=apcommand.accesspoints.atheros.AtherosAR5KAP)
        ap_module.AtherosAR5KAP.return_value = ap_instance
        error_message = 'security setting error'
        ap_instance.set_security.side_effect = Exception(error_message)
        with patch('apcommand.accesspoints.atheros', ap_module):
            self.sub_command.security(args)
            ap_instance.set_security.assert_called_with(type=args.type)
        return
