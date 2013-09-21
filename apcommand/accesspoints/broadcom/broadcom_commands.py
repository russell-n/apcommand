
# python standard library
from abc import ABCMeta, abstractproperty
# this package
from apcommand.baseclass import BaseClass

# this package
from commons import action_dict
from commons import BroadcomWirelessData
from querier import Broadcom5GHzQuerier, Broadcom24GHzQuerier


class BroadcomBaseData(object):
    """
    The base-data to hold the data-dict
    """
    def __init__(self):
        """
        Base Data constructor
        """
        super(BroadcomBaseData, self).__init__()
        self._logger = None
        return

    @classmethod
    def base_data(cls):
        """
        Returns data dictionary that only has action:Apply 
        """
        return action_dict()

    @classmethod
    def base_24_ghz_data(cls):
        """
        data-dictionary to choose the 2.4 GHz interface
        """
        bwd = BroadcomWirelessData
        base_24_ghz_data = cls.base_data()
        base_24_ghz_data[bwd.wireless_interface] = bwd.interface_24_ghz
        return base_24_ghz_data

    @classmethod
    def base_5_ghz_data(cls):
        """
        data-dictionary to chose the 5 Ghz interface
        """
        bwd = BroadcomWirelessData
        base_5_ghz_data = cls.base_data()
        base_5_ghz_data[bwd.wireless_interface] = bwd.interface_5_ghz
        return base_5_ghz_data

    def __repr__(self):
        """
        Returns a representation of the data
        """
        return "{0}: Base: {1} 5GHz: {1} 2.4GHz: {2}".format(self.__class__.__name__,
                                                             self.base_data(),
                                                             self.base_5_ghz_data(),
                                                             self.base_24_ghz_data())


class BroadcomBaseCommand(BaseClass):
    """
    A base-class for the commands
    """
    __metaclass__ = ABCMeta
    def __init__(self, connection):
        """
        BroadcomBaseCommand constructor

        :param:

         - `connection`: A connection to the AP (HTTPConnection)
        """
        self.connection = connection
        self._base_data = None
        self._singular_data = None
        self._data = None
        return

    @abstractproperty
    def base_data(self):
        """
        A data-dictionary to add commands to
        """
        return

    @abstractproperty
    def singular_data(self):
        """
        A data dictionary with the command-specific data
        """
        return

    @property
    def data(self):
        """
        The data dictionary to send to the server
        """
        if self._data is None:
            self._data = self.base_data.copy()
            self._data.update(self.singular_data)
        return self._data




class Base24GHzCommand(BroadcomBaseCommand):
    """
    A base for the 2.4 GHz commands
    """
    def __init__(self, *args, **kwargs):
        super(Base24GHzCommand, self).__init__(*args, **kwargs)
        self._logger = None
        return

    @property
    def base_data(self):
        """
        A data-dictionary that selects the 5 GHz interface
        """
        if self._base_data is None:
            self._base_data = BroadcomBaseData.base_24_ghz_data()
        return self._base_data


class Base5GHzCommand(BroadcomBaseCommand):
    """
    A base for the 5 GHz commands
    """
    def __init__(self, *args, **kwargs):
        super(Base5GHzCommand, self).__init__(*args, **kwargs)
        self._logger = None
        return

    @property
    def base_data(self):
        """
        A data-dictionary that selects the 5 GHz interface
        """
        if self._base_data is None:
            self._base_data = BroadcomBaseData.base_5_ghz_data()
        return self._base_data


# python standard library
import unittest

# third-party
from mock import MagicMock


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

        base_24 = Base24GHzCommand(connection=self.connection)
        data_dict['wl_unit'] = '0'
        self.assertEqual(data_dict, base_24.base_data)
        return

    def test_add(self):
        return
