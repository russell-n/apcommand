
# python standard library
import urlparse
import threading

# this package
from apcommand.baseclass import BaseClass

# third-party
import requests

class EventTimer(BaseClass):
    """
    A timer object to set an event
    """
    def __init__(self, event=None, seconds=0.5):
        """
        EventTimer constructor

        :param:

         - `event`: a threading.Event to set
         - `seconds`: number of seconds to run the timer
        """
        self._event = event
        self.seconds = seconds
        self._timer = None
        return

    @property
    def event(self):
        """
        Threading event for the timer to set
        """
        if self._event is None:
            self._event = threading.Event()
            # I don't know about this, but I think
            # I want it to always rely on the timer to clear it
            self._event.set()
        return self._event

    @property
    def timer(self):
        """
        A threading.Timer object
        """
        # Timers can only be started once, so this can't be persistent
        return threading.Timer(self.seconds, self.set_event)

    def set_event(self):
        """
        Sets the event
        """
        self.event.set()
        return

    def start(self):
        """
        The main interface - clears the event then starts the timer
        """
        self.event.clear()
        self.timer.start()
        return

    def clear(self):
        """
        A convenience method for users to call the event.clear method.        
        """
        self.event.clear()
        return

    def wait(self, timeout=None):
        """
        Calls event.wait if timeout not given use self.seconds
        """
        if timeout is None:
            timeout = self.seconds
        self.event.wait(timeout)
        return            
# end class EventTimer

def wait(method):
    """
    Decorator to wait for previous timers and to start a new one on exit
    """
    def _method(self, *args, **kwargs):
        # wait if timer is running but only up until the time-limit
        self.timer.wait(self.timer.seconds)
        self.timer.clear()
        outcome = method(self, *args, **kwargs)
        self.timer.start()
        return outcome
    return _method

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
                 rest=0.5,
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
         - `rest`: seconds to wait between calls to the server
        """
        super(HTTPConnection, self).__init__()
        self._hostname = None
        self.hostname = hostname
        self.username = username
        self.password = password
        self.rest = rest
        self._protocol = None
        self.protocol = protocol
        self._path = None
        self.path = path
        self.data = data
        self._url = None
        self._lock = lock
        self._timer = None
        return

    @property
    def timer(self):
        """
        An Event Timer to prevent calling the server too soon
        """
        if self._timer is None:
            self._timer = EventTimer(seconds=self.rest)
        return self._timer        

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

    @wait
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
from mock import MagicMock, patch, call

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
        Does calling the HTTPConnection do the same thing as GET?
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
        self.assertEqual(self.url, self.connection.url, "Old URL: {0}, Connection: {1}".format(self.url, self.connection.url))
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

class TestEventTimer(unittest.TestCase):
    def setUp(self):
        self.event_patch = patch('threading.Event')        
        self.mock_event = self.event_patch.start()

        self.timer_patch = patch('threading.Timer')
        self.mock_timer = self.timer_patch.start()
        self.timer = EventTimer()
        return

    def tearDown(self):
        self.event_patch.stop()
        self.timer_patch.stop()
        return

    def test_event(self):
        """
        Does it create then set the event so it won't block by default?
        """
        event = MagicMock()
        e = EventTimer().event
        e.set.assert_called_with()
        return

    def test_set_event(self):
        """
        Does it set the  event?
        """
        self.timer.set_event()
        self.timer.event.set.assert_called_with()
        return

    def test_timer(self):
        """
        Does it pass the timer the seconds and set_event method?
        """
        t = self.timer.timer
        self.mock_timer.assert_called_with(self.timer.seconds, self.timer.set_event)
        return

    def test_start(self):
        """
        Does it clear the event then start the timer?
        """
        self.timer.start()
        # first call - create the event and set
        # second call - clear the call so users will block
        # third call - start the timer
        calls = [call.set(), call.clear(), call.start()]
        self.assertEqual(calls, self.timer.event.mock_calls + self.timer.timer.mock_calls)
        return

    def test_clear(self):
        """
        Does the Timer pass on the clear call to the event?
        """
        self.timer.clear()
        self.timer.event.clear.assert_called_with()
        return

    def test_wait(self):
        """
        Does the Timer pass on the wait call to the event?
        """
        self.timer.wait()        
        self.timer.event.wait.assert_called_with(self.timer.seconds)
        timeout = random.randrange(10)
        self.timer.wait(timeout)
        self.timer.event.wait.assert_called_with(timeout)
        return

class TestWait(unittest.TestCase):
    def setUp(self):
        self.event = MagicMock()
        self.timer = MagicMock()
        self.sleep = random.random()
        self.timer.seconds = self.sleep
        self.cow = MagicMock()
        return
    
    @wait
    def dummy(self, apple):
        return self.cow(apple)

    def test_wait(self):
        """
        Does the decorator call the right methods?
        """
        self.cow.return_value = 'boy'
        output = self.dummy('pie')
        self.cow.assert_called_with('pie')
        self.assertEqual('boy', output)
        calls = [call.wait(self.sleep), call.clear(), call.start()]
        self.assertEqual(calls, self.timer.mock_calls)
        return