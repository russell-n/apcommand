
# python standard library
from abc import ABCMeta, abstractproperty, abstractmethod
# this package
from apcommand.baseclass import BaseClass

# this package
from commons import action_dict, radio_page
from commons import BroadcomWirelessData, BroadcomRadioData
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
    def data(cls, action=True, band=None):
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
        return base_data

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
        super(BroadcomBaseCommand, self).__init__()
        self._logger = None
        self.connection = connection
        self.band = band
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
            self._base_data = BroadcomBaseData.data(band=self.band)
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

    def __iadd__(self, other):
        """
        Adds the other's non_base_data to this added_data

        """
        self.added_data.update(other.non_base_data)
        self._data = self._non_base_data = None
        return self

    def __add__(self, other):
        """
        Adds the other's non_base_data to this added_data

        **For this to work the sub-classes can't change the constructor interface**
        """
        new_object = self.__class__(connection=self.connection,
                                    band=self.band)
        new_object.added_data.update(other.non_base_data)
        return new_object

    def __sub__(self, other):
        """
        Removes the other's non-base data from added_data in new object

        :return: object with this data minus other's non_base_data
        """
        new_object = self.__class__(connection=self.connection,
                                    band=self.band)
        new_object._added_data = self.added_data.copy()
        
        for key in other.non_base_data.iterkeys():
            if key in new_object.added_data:
                del new_object.added_data[key]
        return new_object

    @abstractmethod
    def __call__(self):
        """
        The main method to change settings (probably needs arguments)
        """
        return
# end class BroadcomBaseCommand


class EnableInterface(BroadcomBaseCommand):
    """
    An interface enabler
    """
    def __init__(self, *args, **kwargs):
        super(EnableInterface, self).__init__(*args, **kwargs)
        self._enable_24_data = None
        self._enable_5_data = None
        return

    @radio_page
    def __call__(self):
        """
        Sends the data to the connection 
        """
        self.connection(data=self.data)
        return

    @property
    def singular_data(self):
        """
        The data to enable the 2.4 Ghz interface
        """
        if self._singular_data is None:
            band = str(self.band)
            if band.startswith('2'):
                self._singular_data = self.enable_24_data
            elif band.startswith('5'):
                self._singular_data = self.enable_5_data
        return self._singular_data

    @property
    def enable_5_data(self):
        """
        The data to send to the connection to enable 5 GHz

        :return: dict of data-values for the connection
        """
        if self._enable_5_data is None:
            data = BroadcomWirelessData
            radio_data = BroadcomRadioData
            self._enable_5_data = action_dict()
            self._enable_5_data[data.wireless_interface] = data.interface_5_ghz
            self._enable_5_data[radio_data.interface] = radio_data.radio_on
        return self._enable_5_data


    @property
    def enable_24_data(self):
        """
        The data to send to the connection to enable 2.4 GHz

        :return: dict of data-values for the connection
        """
        if self._enable_24_data is None:
            data = BroadcomWirelessData
            radio_data = BroadcomRadioData
            self._enable_24_data = action_dict()
            self._enable_24_data[data.wireless_interface] = data.interface_24_ghz
            self._enable_24_data[radio_data.interface] = radio_data.radio_on
        return self._enable_24_data


# python standard library
import unittest
import random
import string

# third-party
from mock import MagicMock


random_letters = lambda: ",".join((random.choice(string.letters) for char in xrange(random.randint(1,5))))


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

    def path(self):
        return

# this can't be random in the class for testing to work
# Because __add__  creates a new object
test_data = {random_letters(): random_letters()}
test_data_2 = {random_letters(): random_letters()}
test_data_3 = {random_letters(): random_letters()}    
class TestChild(BroadcomBaseCommand):
    def __init__(self, *args, **kwargs):
        super(TestChild, self).__init__(*args, **kwargs)
        return

    @property
    def singular_data(self):
        if self._singular_data is None:
            self._singular_data = test_data
        return self._singular_data

    def __call__(self):
        return

    def __add__(self, other):
        t = TestChild(self.connection)
        t.added_data.update(other.non_base_data)
        return t

    def path(self):
        return

class TestChild2(TestChild):
    def __init__(self, *args, **kwargs):
        super(TestChild2, self).__init__(*args, **kwargs)
        return

    @property
    def singular_data(self):
        if self._singular_data is None:
            self._singular_data = test_data_2
        return self._singular_data

class TestChild3(TestChild):
    def __init__(self, *args, **kwargs):
        super(TestChild3, self).__init__(*args, **kwargs)
        return

    @property
    def singular_data(self):
        if self._singular_data is None:
            self._singular_data = test_data_3
        return self._singular_data
    
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

    def test_add(self):
        """
        Can you add two commands?        
        """
        command_1 = TestChild(self.connection)
        command_2 = TestChild2(self.connection)
        
        data_1, data_2 = command_1.data, command_2.data

        data_changed = data_1.copy()
        data_changed.update(data_2)

        # first __add__
        command_3 = command_1 + command_2

        # creates a new object with the combined data
        self.assertEqual(data_changed, command_3.data)
        self.assertEqual(self.connection, command_3.connection)
        # leaves the originals alone
        self.assertEqual(command_1.data, data_1)
        self.assertEqual(command_2.data, data_2)

        # now __iadd__
        command_1 += command_2
        # changes LHS in place
        self.assertEqual(command_1.data, data_changed)
        self.assertEqual(command_2.data, data_2)
        return

    def test_subtract(self):
        """
        Can you subtract two commands?
        """
        command_1 = TestChild(self.connection)
        command_2 = TestChild2(self.connection)
        command_3 = TestChild3(self.connection)

        data_1, data_2, data_3 = command_1.data, command_2.data, command_3.data
        data_changed = data_1.copy()
        data_changed.update(data_2)
        data_changed.update(data_3)

        # first add so the commands are different
        command_1 += command_2
        command_1 += command_3
        
        # First __sub__
        command_4 = command_1 - command_2

        data_1_3 = data_1.copy()
        data_1_3.update(data_3)
        # new cleaned object
        self.assertEqual(command_4.data, data_1_3)

        command_4 = command_1 - command_2 - command_3
        self.assertEqual(command_4.data, data_1)

        # old objects unchanged
        self.assertEqual(command_1.data, data_changed)
        self.assertEqual(command_2.data, data_2)

        # now __isub__
        self.assertNotEqual(command_1.data, data_1)
        command_1 -= command_2
        self.assertEqual(command_1.data, data_1_3)
        self.assertEqual(command_2.data, data_2)

        command_1 -= command_3
        self.assertEqual(command_1.data, data_1)
        return
        


class TestEnableInterface(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        return

    def test_24ghz(self):
        """
        Does it construct the right set of data to disable the interface?
        """
        command = EnableInterface(connection=self.connection,
                                  band='2.4')
        expected_data =  {'wl_unit':'0',
                          'action':'Apply',
                          'wl_radio':'1'}

        self.assertEqual(command.singular_data, expected_data)
        command()
        self.assertEqual(self.connection.path, 'radio.asp')
        self.connection.assert_called_with(data=expected_data)
        return

    def test_5_ghz(self):
        """
        Does it send the 5 GHz data to the connection?
        """
        command = EnableInterface(connection=self.connection,
                                  band='5')
        expected_data ={'action':'Apply',
                        'wl_unit':'1',
                        'wl_radio':'1'}
        self.assertEqual(command.singular_data, expected_data)
        return
