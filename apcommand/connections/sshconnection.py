
#python Libraries
import socket
import os

# third-party libraries
import paramiko

# arachne Libraries
from apcommand.commons.readoutput import ValidatingOutput
from apcommand.baseclass import BaseClass
from apcommand.commons import errors

ConnectionError = errors.ConnectionError

# connections
from nonlocalconnection import NonLocalConnection, NonLocalConnectionBuilder
from localconnection import OutputError


PLUGIN_NAME = 'ssh'
SPACER = '{0} {1}'
UNKNOWN = "Unknown command: "
EOF = ''
SPACE = ' '
DOT_JOIN = "{0}.{1}"
NEWLINE = "\n"


class SSHClient(paramiko.SSHClient):
    """
    Subclasses paramiko's SSHClient to add a timeout.
    """
    def exec_command(self, command, timeout=None, bufsize=-1, combine_stderr=False):
        """
        :param:

         - `command`: A string to send to the client.
         - `timeout`: Set non-blocking timeout.
         - `bufsize`: Interpreted same way as python `file`.
         - `combine_stderr`: Sets the paramiko flag so there's only one stream

        :rtype: tuple
        :return: stdin, stdout, stderr
        """
        channel = self._transport.open_session()
        channel.settimeout(timeout)
        channel.exec_command(command)
        stdin = channel.makefile('wb', bufsize)
        stdout = channel.makefile('rb', bufsize)
        if combine_stderr:
            channel.set_combine_stderr(combine_stderr)
            stderr = stdout
        else:
            stderr = channel.makefile_stderr('rb', bufsize)
        return stdin, stdout, stderr

    def invoke_shell(self, term='vt100', width=80, height=24, timeout=None, bufsize=-1):
        """
        :param:

         - `term`: Terminal to emulate.
         - `width`: Screen width
         - `height`: Screen Height.
         - `timeout`: Set non-blocking timeout.
         - `bufsize`: Interpreted same way as python `file`.

        :rtype: tuple
        :return: stdin, stdout, stderr
        """
        channel = self._transport.open_session()
        channel.settimeout(timeout)
        channel.get_pty(term, width, height)
        channel.invoke_shell()
        stdin = channel.makefile('wb', bufsize)
        stdout = channel.makefile('rb', bufsize)
        stderr = channel.makefile_stderr('rb', bufsize)
        return stdin, stdout, stderr

    def invoke_shell_rw(self, term='vt100', width=80, height=24, timeout=None, bufsize=-1):
        """
        :param:

         - `term`: Terminal to emulate.
         - `width`: Screen width
         - `height`: Screen Height.
         - `timeout`: Set non-blocking timeout.
         - `bufsize`: Interpreted same way as python `file`.

        :rtype: tuple
        :return: i/o
        """
        channel = self._transport.open_session()
        channel.settimeout(timeout)
        channel.set_combine_stderr(True)
        channel.get_pty(term, width, height)
        channel.invoke_shell()

        shell = channel.makefile('r+b', bufsize)
        return shell
#end class SSHClient


class SimpleClient(BaseClass):
    """
    A simple wrapper around paramiko's SSHClient.

    The only intended public interface is exec_command.
    """
    def __init__(self, hostname, username, password=None, port=22, timeout=5):
        """
        :param:

         - `hostname`: ip address or resolvable hostname.
         - `username`: the login name.
         - `password`: optional if ssh-keys are set up.
         - `port`: The port for the ssh process.
         - `timeout`: Time to give the client to connect
        """
        super(SimpleClient, self).__init__()
        self._logger = None
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self._client = None
        return

    def exec_command(self, command, timeout=10):
        """
        A pass-through to the SSHClient's exec_command.

        :param:

         - `command`: A string to send to the client.
         - `timeout`: Set non-blocking timeout.

        :rtype: tuple
        :return: stdin, stdout, stderr

        :raise: ConnectionError for paramiko or socket exceptions
        """
        if not command.endswith(NEWLINE):
            command += NEWLINE
        try:
            return self.client.exec_command(command, timeout)

        except paramiko.SSHException as error:
            self._client = None
            self.logger.error(error)
            raise ConnectionError("There is a problem with the ssh-connection to:\n {0}".format(self))
        except paramiko.PasswordRequiredException as error:
            self.logger.error(error)
            self.logger.error("Private Keys Not Set Up, Password Required.")
            raise ConnectionError("SSH Key Error :\n {0}".format(self))
        except socket.error as error:
            self.logger.error(error)
            if 'Connection refused' in error: 
                raise ConnectionError("SSH Server Not responding: check setup:\n {0}".format(self))
            raise ConnectionError("Problem with:\n {0}".format(self))
        return
        
    @property
    def client(self):
        """
        :rtype: paramiko.SSHClient
        :return: An instance of SSHClient connected to remote host.
        :raise: ClientError if the connection fails.
        """
        if self._client is None:
            self._client = SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._client.load_system_host_keys()
            try:
                self._client.connect(hostname=self.hostname,
                                     port=self.port,
                                     username=self.username,
                                     password=self.password,
                                     timeout=self.timeout)
            except paramiko.AuthenticationException as error:
                self.logger.error(error)
                raise ConnectionError("There is a problem with the ssh-keys or password for \n{0}".format(self))
            except socket.timeout as error:
                self.logger.error(error)
                raise ConnectionError("Paramiko is unable to connect to \n{0}".format(self))
        return self._client

    def __str__(self):
        """
        :return: username, hostname, port, password in string
        """
        user = "Username: {0}".format(self.username)
        host = "Hostname: {0}".format(self.hostname)
        port = "Port: {0}".format(self.port)
        password = "Password: {0}".format(self.password)
        return NEWLINE.join([user, host, port, password])

    def close(self):
        """
        :postcondition: client's connection is closed and self._client is None                
        """
        self.client.close()
        self._client = None
        return
# class SimpleClient


class SSHConnection(NonLocalConnection):
    """
    An SSHConnection executes commands over an SSHConnection
    """
    def __init__(self, port=None, 
                 *args, **kwargs):
        """
        SSHConnection Constructor
        
        :param:

         - `port`: The ssh port
        """
        super(SSHConnection, self).__init__(*args, **kwargs)
        self._port = port
        self.port = port
        return

    @property
    def port(self):
        """
        The server-port

        :rtype: Integer
        :return: port number
        """
        if self._port is None:
            self._port = 22
        return self._port

    @port.setter
    def port(self, port):
        """
        Sets the port number

        :param:

         - `port`: An integer port-number for the SSH Server
        """
        self._port = port
        return

    @property
    def client(self):
        """
        The SSH client
        
        :return: SimpleClient for the SSHConnection
        """
        if self._client is None:
            self._client = SimpleClient(hostname=self.hostname, username=self.username,
                                        password=self.password, port=self.port,
                                        timeout=self.timeout)
        return self._client
    

    def _main(self, command, arguments, timeout):
        """
        This implements the NonLocalConnection abstract method
        
         * runs the SimpleClient exec_command

        :param:

         - `command`: The shell command.
         - `arguments`: A string of command arguments.
         - `timeout`: readline timeout for the SSHConnection
        :return: OutputError with output and error file-like objects
        """
        self.logger.debug("command: {0}, arguments: {1}".format(command,
                                                                arguments))
        self.logger.debug("calling client.exec_command")
            
        stdin, stdout, stderr = self.client.exec_command(SPACER.format(command, arguments), timeout=timeout)

        self.logger.debug("Completed exec_command of: {0} {1}".format(command, arguments))
        return OutputError(OutputFile(stdout, self.check_errors), OutputFile(stderr, self.check_errors))

    def check_errors(self, line):
        """
        Doesn't do anything - SSHClient handles ssh errors. Overwrite in sub-classes if needed
        """
        return
    
    def __str__(self):
        return "{0} ({1}): {2}@{3} ".format(self.__class__.__name__, self.operating_system, self.username, self.hostname)
# end class SSHConnection


class OutputFile(ValidatingOutput):
    """
    A class to handle the ssh output files

    This traps socket timeouts.
    """
    def __init__(self, *args, **kwargs):
        super(OutputFile, self).__init__(*args, **kwargs)
        return

    def readline(self, timeout=10):
        """
        :param:

         - `timeout`: The length of time to wait for output

        :return: line from readline, EOF or None (in event of timeout)
        """
        if not self.empty:
            try:
                line = self.lines.readline()
                if line == EOF:
                    self.end_of_file = True
                self.validate(line)
                return line
            except socket.timeout:
                self.logger.debug("socket.timeout")
                return SPACE
        return EOF
# end class OutputFile


class SSHConnectionBuilder(NonLocalConnectionBuilder):
    """
    Implements a builder for the SSHConnection
    """
    def __init__(self, *args, **kwargs):
        """
        SSHConnectionBuilder Constructor

        :param:

         - `parameters`: namedtuple of parameters to build the connection
        """
        super(SSHConnectionBuilder, self).__init__(*args, **kwargs)
        return

    @property
    def port(self):
        """
        Port for the SSH-server

        :return: the SSHParameters.port value
        """
        if self._port is None:
            self._port = self.parameters.port
        return self._port
    
    @property
    def operating_system(self):
        """
        :return: parameters.operating_system
        """
        if self._operating_system is None:
            try:
                self._operating_system = self.parameters.operating_system
            except AttributeError as error:
                self.logger.debug(error)
                self.logger.warning("Operating System not found in: {0}".format(self.parameters))
        return self._operating_system

    @property
    def library_path(self):
        """
        :return: LD_LIBRARY_PATH value(s) or None
        """
        if self._library_path is None:
            try:
                self._library_path = ":".join(self.parameters.library_path.split())
            except AttributeError as error:
                self.logger.debug(error)
        return self._library_path

    @property
    def path(self):
        """
        :return: additions to the PATH
        """
        if self._path is None:
            try:
                self._path = ":".join(self.parameters.path.split())
            except AttributeError as error:
                self.logger.debug(error)
        return self._path
    
    @property
    def hostname(self):
        """
        The hostname parameter extracted from the parameters
        
        :rtype: StringType
        :return: The hostname (I.P.) to connect to
        :raise: ConfigurationError if not set
        """
        if self._hostname is None:
            try:
                self._hostname = self.parameters.hostname
            except AttributeError as error:
                self.logger.debug(error)
                try:
                    self._hostname = self.parameters.address
                except AttributeError as error:
                    self.logger.debug(error)
                    raise errors.ConfigurationError("`hostname` is a required parameter for the SSHConnection")
        return self._hostname

    @property
    def username(self):
        """
        :rtype: StringType
        :return: user login name
        :raise: ConfigurationError if not found
        """
        if self._username is None:
            try:
                self._username = self.parameters.username
            except AttributeError as error:
                self.logger.debug(error)
                try:
                    self._username = self.parameters.login
                except AttributeError as error:
                    self.logger.debug(error)
                    raise errors.ConfigurationError("`username` is a required parameter for the SSHConnection")                
        return self._username

    @property
    def password(self):
        """
        :return: the password for the connection (sets to None if not given in the parameters)
        """
        if self._password is None:
            try:
                self._password = self.parameters.password
            except AttributeError as error:
                self.logger.debug(error)
                self._password = None
        return self._password
    
    @property
    def product(self):
        """
        Implements the builder.product attribute
        
        :return: an SSHConnection
        """
        if self._product is None:
            self.logger.debug("Creating the ssh connection.")
            self._product = SSHConnection(hostname=self.hostname,
                                                           username=self.username,
                                                           password=self.password,
                                                           port=self.port,
                                                           path=self.path,
                                                           library_path=self.library_path,
                                                           operating_system=self.operating_system)
        return self._product
# end class SshConnectionBuilder


# python standard library
import unittest
from types import StringType

# third-party
#from yapsy.PluginManager import PluginManagerSingleton

#arachne
#from arachne import PLUGIN_PLACES
#from arachne import PLUGIN_EXTENSION
#from arachne import CONNECTION_CATEGORY
#
from nonlocalconnection import ConnectionParameters

EMPTY_STRING = ''


class TestSSHConnectionBuilder(unittest.TestCase):
    pass
#    def setUp(self):
#        self.plugin_manager = PluginManagerSingleton.get()
#        self.plugin_manager.setPluginPlaces(PLUGIN_PLACES)
#        self.plugin_manager.setPluginInfoExtension(PLUGIN_EXTENSION)
#        self.plugin_manager.setCategoriesFilter({CONNECTION_CATEGORY:NonLocalConnectionBuilder})
#        self.plugin_manager.collectPlugins()
#        return
#        
#    def test_plugin(self):
#        """
#        Is the plugin discoverable?
#        """
#        builder = self.plugin_manager.getPluginByName(PLUGIN_NAME, CONNECTION_CATEGORY)
#        self.assertIsNotNone(builder)
#        # yapsy mangles the class-name so the is-instance assertion won't work
#        #self.assertIsInstance(builder.plugin_object, SSHConnectionBuilder)
#        self.assertEqual(PLUGIN_NAME, builder.name)
#        return
#
#    def test_product(self):
#        """
#        Does it build the SSHConnection correctly?
#        """
#        hostname = 'localhost'
#        username = 'bob'
#        password = 'ummagumma'
#        operating_system = 'beos'
#        path = "/home/bob/bin"
#        library_path = '/var/lib'
#        port = 5050
#        parameters = ConnectionParameters(hostname=hostname, username=username,
#                                   password=password, operating_system=operating_system,
#                                   path=path, library_path=library_path, port=port)
#
#        builder = self.plugin_manager.getPluginByName(PLUGIN_NAME, CONNECTION_CATEGORY).plugin_object
#        builder.parameters = parameters
#        connection = builder.product
#
#        self.assertEqual(connection.hostname, hostname)
#        self.assertEqual(connection.username, username)
#        self.assertEqual(connection.password, password)
#        self.assertEqual(connection.operating_system, operating_system)
#        self.assertEqual(connection.path, 'PATH=' + path + ":$PATH;")
#        self.assertEqual(connection.library_path, 'export LD_LIBRARY_PATH=' +
#                         library_path + ':$LD_LIBRARY_PATH;')
#        self.assertEqual(connection.port, port)
#        return
#
#    def test_defaults(self):
#        """
#        If you only pass in the required parameters, will the defaults be used?
#        """
#        hostname = 'localhost'
#        username = 'bob'
#
#        password = None
#        operating_system = None
#        path = None
#        library_path = None
#        port = None
#        parameters = ConnectionParameters(hostname=hostname, username=username,
#                                   password=password, operating_system=operating_system,
#                                   path=path, library_path=library_path, port=port)
#
#        builder = self.plugin_manager.getPluginByName(PLUGIN_NAME, CONNECTION_CATEGORY).plugin_object
#        builder.parameters = parameters
#        connection = builder.product
#
#        self.assertEqual(connection.hostname, hostname)
#        self.assertEqual(connection.username, username)
#        self.assertEqual(connection.password, password)
#        self.assertEqual(connection.operating_system, operating_system)
#        self.assertEqual(connection.path, EMPTY_STRING)
#        self.assertEqual(connection.library_path, EMPTY_STRING)
#        self.assertEqual(connection.port, 22)
#        return
#


if __name__ == "__main__":
    import pudb; pudb.set_trace()
    plugin_manager = PluginManagerSingleton.get()
    plugin_manager.setPluginPlaces(PLUGIN_PLACES)
    plugin_manager.setPluginInfoExtension(PLUGIN_EXTENSION)
    plugin_manager.setCategoriesFilter({CONNECTION_CATEGORY:NonLocalConnectionBuilder})
    plugin_manager.collectPlugins()
    builder = plugin_manager.getPluginByName(PLUGIN_NAME, CONNECTION_CATEGORY)
    hostname = 'localhost'
    username = 'bob'
    password = 'ummagumma'
    operating_system = 'beos'
    path = "/home/bob/bin"
    library_path = '/var/lib'
    port = 5050
    parameters = ConnectionParameters(hostname=hostname, username=username,
                                   password=password, operating_system=operating_system,
                                   path=path, library_path=library_path, port=port)

    print plugin_manager.getAllPlugins()
    builder = plugin_manager.getPluginByName(PLUGIN_NAME, CONNECTION_CATEGORY).plugin_object
    builder.parameters = parameters    
    connection = builder.product
    hostname = connection.hostname

 
