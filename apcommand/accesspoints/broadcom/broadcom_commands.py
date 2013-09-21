
# python standard library
from abc import ABCMeta, abstractproperty, abstractmethod
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
        base_24_ghz_data = {bwd.wireless_interface: bwd.interface_24_ghz}
        return base_24_ghz_data

    @classmethod
    def base_5_ghz_data(cls):
        """
        data-dictionary to chose the 5 Ghz interface
        """
        bwd = BroadcomWirelessData
        base_5_ghz_data = {bwd.wireless_interface:bwd.interface_5_ghz}
        return base_5_ghz_data

    @classmethod
    def __call__(cls, action=True, band=None):
        """
        Builds a data-dict based on action and band

        :param:

         - `action`: if True, add action:Apply to the dict
         - `band`: if 2.4 or 5 add the interface selection data

        :return: base data-dict
        """
        band = str(band)
        if action:
            base_data = cls.base_data()
        else:
            base_data = {}

        if band.startswith('2'):
            base_data.update(cls.base_24_ghz_data())
        elif band.startswith('5'):
            base_data.update(cls.base_5_ghz_data())
        return

    def __repr__(self):
        """
        Returns a representation of the data
        """
        return "{0}: Base: {1} 5GHz: {1} 2.4GHz: {2}".format(self.__class__.__name__,
                                                             self.base_data(),
                                                             self.base_5_ghz_data(),
                                                             self.base_24_ghz_data())


class BroadcomBaseQuery(BaseClass):
    """
    A base to query the server
    """
    __metaclass__ = ABCMeta
    def __init__(self, connection, band=None):        
        """
        BroadcomBaseQuery constructor

        :param:

         - `connection` : a connection to the AP
         - `band`: 2.4, 5 or None (depending on the page)
        """
        self.connection = connection
        self.band = band
        self._data = None
        self._query = None
        return

    @property
    def data(self):
        """
        Data dictionary to give to the server
        """
        if self._data is None:
            self._data = BroadcomBaseData(action=False,
                                          band=self.band)
        return self._data

    @abstractproperty
    def query(self):
        """
        A querier to interpret the output of the connection
        """
        return

    @abstractmethod
    def __call__(self):
        """
        The main method to query the server
        """
        return    


class BroadcomBaseCommand(BaseClass):
    """
    A base-class for the commands that change settings
    """
    __metaclass__ = ABCMeta
    def __init__(self, connection, band=None):
        """
        BroadcomBaseCommand constructor

        :param:

         - `connection`: A connection to the AP (HTTPConnection)
         - `band`: 2.4, 5, or None (chooses the data-dictionary)
        """
        self.connection = connection
        self._base_data = None
        self._singular_data = None
        self._added_data = None
        self._non_base_data = None
        self._data = None
        return

    @property
    def base_data(self):
        """
        A data-dictionary to add commands to
        """
        if self._base_data is None:
            self._base_data = BroadcomBaseData(action=True,
                                               band=self.band)
        return self._base_data

    @abstractproperty
    def singular_data(self):
        """
        A data dictionary with the command-specific data (or empty if querying)
        """
        if self._singular_data is None:
            self._singular_data = {}
        return self._singular_data    

    @property
    def added_data(self):
        """
        Maintains data added from other commands
        """
        if self._added_data is None:
            self._added_data = {}
        return self._added_data

    @property
    def non_base_data(self):
        """
        The singular data updated with any added data
        """
        if self._non_base_data is None:
            self._non_base_data = self.singular_data.copy()
            self._non_base_data.update(self.added_data)
        return self._non_base_data

    @property
    def data(self):
        """
        The data dictionary to send to the server
        """
        if self._data is None:
            self._data = self.base_data.copy()
            self._data.update(self.non_base_data)
        return self._data

    def __add__(self, other):
        """
        Adds the other's non_base_data to this added_data

        """
        self.added_data.update(other.non_base_data)
        self._data = self._non_base_data = None
        return

    def __sub__(self, other):
        """
        Removes the other's non-base data from added_data
        """
        for key in other.non_base_data.iterkeys():
            if key in self.added_data:
                del self.added_data[key]
        self._data = self._non_base_data = None
        return

    @abstractmethod
    def __call__(self):
        """
        The main method to change settings (probably needs arguments)
        """
        return


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

    @property
    def singular_data(self):
        return
    
    def __call__(self):
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

    #def test_base_commands(self):
    #    """
    #    Do the band-specific base-commands build the right data and queries?
    #    """
    #    base_5 = Base5GHzCommand(connection=self.connection)
    #    data_dict = action_dict()
    #    data_dict['wl_unit'] = '1'
    #    self.assertEqual(data_dict, base_5.base_data)
    #
    #    base_24 = Base24GHzCommand(connection=self.connection)
    #    data_dict['wl_unit'] = '0'
    #    self.assertEqual(data_dict, base_24.base_data)
    #    return

    def test_add(self):
        return
