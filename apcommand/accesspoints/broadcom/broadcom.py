
# this package
from apcommand.baseclass import BaseClass


class BroadcomBCM94718NR(BaseClass):
    """
    A class to control and query the Broadcom BCM94718NR
    """
    def __init__(self, hostname):
        """
        BroadcomBCM94718NR Constructor

        :param:

         - `hostname`: address of the AP
        """
        self.hostname = hostname
        return


# python standard library
import unittest


class TestBroadcomBCM94718NR(unittest.TestCase):
    def setUp(self):
        self.hostname = '192.168.1.1'
        self.control = BroadcomBCM94718NR(hostname=self.hostname)
        return

    def test_constructor(self):
        """
        Does it construct the control correctly?
        """
        self.assertEqual(self.hostname, self.control.hostname)
        return
    
    def test_enable_24_interface(self):
        """
        Does it enable the 2.4 GHz interface?
        """
        return
    
