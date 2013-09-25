
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
import apcommand.accesspoints.broadcom.broadcom
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

        :return: AP Controller
        '''
        # assume that the accesspoint class has valuable defaults
        # only pass in parameters that have been set by the arguments
        apargs = ('hostname', 'username', 'password', 'sleep')
        apvalues = (getattr(args, arg) for arg in apargs if getattr(args, arg) is not None)
        apkeys = (arg for arg in apargs if getattr(args, arg) is not None)
        apkwargs = dict(zip(apkeys, apvalues))
        
        ap = apcommand.accesspoints.broadcom.broadcom.BroadcomBCM94718NR(**apkwargs)
        return ap


    @try_except
    def status(self, args):
        """
        Calls the access-point control's status method

        :param:

         - `args`: namespace with 'interface' attribute
        """
        ap = self.access_point(args)
        if args.band is not 'all':
            print "{0} GHz".format(args.band)
            print ap.get_status(args.band)
        else:
            print ap.get_status(args.band)
        return

    @try_except
    def channel(self, args):
        """
        Calls the access point's set_channel method (unless channel not set, then get_channel)

        :param:

         - `args`: namespace with `channel` attribute
        """
        ap = self.access_point(args)
        if args.channel is None:
            out_string = "{0} GHz Channel: {1} {3} ({2})"
            for band in '2.4 5'.split():
                print "{0} GHz:".format(band)
                key = band[0]
                channel = ap.query[key].channel
                print "   Channel: {0}".format(channel)
                state = ap.query[key].state
                print "  {0}".format(state)
                sideband = ap.query[key].sideband
                if sideband is None:
                    sideband = ''
                print '   {0}'.format(sideband)

                self.logger.debug(out_string.format(band, channel, state, sideband))
        else:
            ap.set_channel(channel=args.channel)
        return

    @try_except
    def ssid(self, args):
        """
        Calls the access point's set_ssid method

        :param:

         - `args`: namespace with `band` and `ssid` attributes
        """
        ap = self.access_point(args)
        indent = ' ' * 3
        if args.band is None:
            if args.ssid is not None:
                print "Need band to change ssid"
                return
            print "2.4 GHz:"
            print indent + ap.get_ssid('2.4')
            print "5 GHz:"
            print indent + ap.get_ssid('5')
        elif args.ssid is None:
            print "{0} GHz:".format(args.band)
            print indent + ap.get_ssid(args.band)
        else:
            ap.set_ssid(ssid=args.ssid, band=args.band)
        return

    @try_except
    def security(self, args):
        """
        calls the AP's set_security method

        :param:

         - `args`: namespace with `type` attribute
        """
        ap = self.access_point(args)
        ap.set_security(security_type=args.type)
        return

    @try_except
    def command(self, args):
        """
        Calls the AP's exec_command method

        :param:

         - `args`: namespace with `command` attribute
        """
        ap = self.access_point(args)
        ap.exec_command(args.command)
        return

    @try_except
    def ipaddress(self, args):
        """
        Sets the AP's ip address

        :param:

         - `args`: namespace with `ipaddress`, `subnetmask` attributes
        """
        ap = self.access_point(args)
        ap.set_ip(address=args.ipaddress,
                  mask=args.subnetmask)
        return

    @try_except
    def enable(self, args):
        """
        Enables an AP interface

        :param:

         - `args`: namespace with `interface` attribute
        """
        ap = self.access_point(args)
        ap.enable(interface=args.interface)
        return
        
