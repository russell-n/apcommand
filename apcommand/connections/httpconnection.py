
# python standard library
import urlparse
import threading

# this package
from apcommand.baseclass import BaseClass

# third-party
import requests


PROTOCOL = 'http'
GET = 'GET'
EMPTY_STRING = ''


class HTTPConnectionError(RuntimeError):
   """An exception to raise if the server wasn't reachable."""


class HTTPConnection(BaseClass):
    """
    Acts as a client connection to an HTTP server
    """
    def __init__(self, hostname, username=EMPTY_STRING, password=EMPTY_STRING,
                 path=EMPTY_STRING, data=None, protocol=PROTOCOL,
                 lock=None):
        """
        HTTPConnection constructor

        :param:

         - `hostname`: Address or resolvable host-name (e.g. www.google.com)
         - `username`: Username for sites that need authentication
         - `password`: password for sites needing authentication
         - `path`: optional path to add to URL
         - `protocol`: transport protocol (most likely 'http')
         - `data`: dictionary of data for the page
         - `lock`: A re-entrant lock for users of the connection to share
        """
        super(HTTPConnection, self).__init__()
        self._hostname = None
        self.hostname = hostname
        self.username = username
        self.password = password
        self._protocol = None
        self.protocol = protocol
        self._path = None
        self.path = path
        self.data = data
        self._url = None
        self._lock = lock
        return

    @property
    def lock(self):
        """
        A re-entrant lock for clients to share

        :rtype: RLock
        """
        if self._lock is None:
            self._lock = threading.RLock()
        return self._lock

    @property
    def protocol(self):
        """
        The protocol for the URL (probabl http, maybe ftp)
        """
        return self._protocol

    @protocol.setter
    def protocol(self, new_protocol):
        """
        Sets the protocol, resets the url
        """
        self._protocol = new_protocol.lower()
        self._url = None
        return

    @property
    def hostname(self):
        """
        The address for the HTTP server
        """
        return self._hostname

    @hostname.setter
    def hostname(self, new_hostname):
        """
        Sets the hostname and resets the URL
        """
        self._hostname = new_hostname
        self._url = None
        return

    @property
    def path(self):
        """
        A path-string for the URL
        """
        return self._path

    @path.setter
    def path(self, new_path):
        """
        Sets the path and re-sets the url
        """
        self._path = new_path
        self._url = None
        return

    @property
    def url(self):
        """
        The URL for the server
        """
        if self._url is None:
            self._url = urlparse.urlunparse((self.protocol, self.hostname,
                                             self.path, EMPTY_STRING,
                                             EMPTY_STRING, EMPTY_STRING))
                                             
        return self._url

    def request(self, method, *args, **kwargs):
        """
        Calls requests.request(method, *args, **kwargs)

        :return: requests.Response object
        """
        try:
            if 'data' not in kwargs and self.data is not None:
                return requests.request(method, self.url, data=self.data,
                                        auth=(self.username, self.password), *args, **kwargs)
            return requests.request(method, self.url,
                                    auth=(self.username, self.password), *args, **kwargs)
        except requests.ConnectionError as error:
            self.logger.error(error)
            self.logger.error("Check the server and the sleep times between requests")
        raise HTTPConnectionError("Unable to connect to the server")

    def __call__(self, *args, **kwargs):
        """
        A shortcut for GET requests

        :return: requests.Response object
        """
        return self.request(GET, *args, **kwargs)
        
    
    def __getattr__(self, method):
        """
        The parameters are the same as `requests.request` (method is converted to uppercase)
        
        :param:

         - `method`: The HTTP Method (GET, POST, HEAD, PATCH, DELETE)

        :return: requests.request method called with passed-in args and kwargs
        """
        def request_call(*args, **kwargs):
            return self.request(method.upper(), *args, **kwargs)

        return request_call
    


# python standard library
import unittest
from random import randrange
import random
choose = random.choice
import string

# third-party
from mock import MagicMock, patch


random_letters = lambda : ''.join([choose(string.letters) for choice in xrange(randrange(100))])
class TestHTTPConnection(unittest.TestCase):
    def setUp(self):
        self.hostname = '192.168.1.1'
        self.username = random_letters()
        self.password = random_letters()
        self.auth = (self.username, self.password)
        self.data = {"wl_unit":'0'}
        self.path = 'radio.asp'
        self.url = 'http://' + self.hostname + '/' + self.path
        self.connection = HTTPConnection(hostname=self.hostname,
                                         username=self.username,
                                         password=self.password,
                                         data=self.data,
                                         path=self.path)

        # mocks
        self.requests = MagicMock()
        self.response = MagicMock()
        self.requests.return_value = self.response
        return

    def test_constructor(self):
        """
        Does the constructor match the signature?
        """
        self.assertEqual(self.hostname, self.connection.hostname)
        self.assertEqual(self.path, self.connection.path)
        self.assertEqual(self.username, self.connection.username)
        self.assertEqual(self.password, self.connection.password)
        
        self.assertEqual(self.url,
                         self.connection.url)
        self.assertEqual(self.data,
                         self.connection.data)
        return

    def test_request(self):
        """
        Does it call requests.request with the right signature?
        """
        with patch('requests.request', self.requests):
            # get
            outcome = self.connection.get()
            self.assertIsNotNone(self.connection.data)
            self.requests.assert_called_with('GET', self.connection.url,
                                                  auth=self.auth,
                                                  data=self.data)
            self.assertEqual(outcome, self.response)
            # post
            params = {'xor':'1', 'aor':'0'}
            self.connection.data = None
            outcome = self.connection.post(params=params)
            self.requests.assert_called_with('POST', self.connection.url,
                                             auth=self.auth,
                                             params=params)
            self.assertEqual(outcome, self.response)
        return

    def test_call(self):
        """
        Does the calling the HTTPConnection do the same thing as GET?
        """
        with patch('requests.request', self.requests):
            data = {'wl_radio':'1'}
            outcome = self.connection(data=data)
            self.requests.assert_called_with(GET, self.url, auth=self.auth,
                                             data=data)
        return

    def test_set_parameter(self):
        """
        Does setting parameters that affect the url reset it?
        """
        new_path = random_letters()
        self.assertEqual(self.url, self.connection.url)
        self.connection.path = new_path
        new_url = self.url.replace(self.path, new_path)
        self.assertEqual(new_url,
                         self.connection.url)
        new_hostname = random_letters()

        self.connection.hostname = new_hostname
        new_url = new_url.replace(self.hostname, new_hostname)
        self.assertEqual(new_url, self.connection.url)

        new_protocol = random_letters()
        new_url = new_url.replace(PROTOCOL, new_protocol.lower())
        self.connection.protocol = new_protocol
        self.assertEqual(new_url,
                         self.connection.url)
        return

