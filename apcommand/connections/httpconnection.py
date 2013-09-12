
# python standard library
import urlparse
# this package
from apcommand.baseclass import BaseClass

# third-party
import requests


PROTOCOL = 'http'
GET = 'GET'
EMPTY_STRING = ''


class HTTPConnection(BaseClass):
    """
    Acts as a client connection to an HTTP server
    """
    def __init__(self, hostname, username=EMPTY_STRING, password=EMPTY_STRING,
                 protocol=PROTOCOL, path=EMPTY_STRING):
        """
        HTTPConnection constructor

        :param:

         - `hostname`: Address or resolvable host-name (e.g. www.google.com)
         - `username`: Username for sites that need authentication
         - `password`: password for sites needing authentication
         - `path`: optional path to add to URL
         - `protocol`: transport protocol (most likely 'http')
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.protocol = protocol
        self.path = path
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
        return requests.request(method, self.url,
                                auth=(self.username, self.password), *args, **kwargs)

    def __call__(self, *args, **kwargs):
        """
        A shortcut for GET requests

        :return: requests.Response object
        """
        return requests.request(GET, self.url,
                                auth=(self.username, self.password), *args, **kwargs)

    
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
        self.path = 'radio.asp'
        self.url = 'http://' + self.hostname + '/' + self.path
        self.connection = HTTPConnection(hostname=self.hostname,
                                         username=self.username,
                                         password=self.password,
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
        return

    def test_request(self):
        """
        Does it call requests.request with the right signature?
        """
        with patch('requests.request', self.requests):
            # get
            outcome = self.connection.get()
            self.requests.assert_called_with('GET', self.connection.url,
                                                  auth=self.auth)
            self.assertEqual(outcome, self.response)
            # post
            params = {'xor':'1', 'aor':'0'}
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
            data = {'wl_radio':'0'}
            outcome = self.connection(data=data)
            self.requests.assert_called_with('GET', self.url, auth=self.auth,
                                             data=data)
            return

