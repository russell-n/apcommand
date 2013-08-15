
class OperatorError(Exception):
    """An OperatorError should be fatal to the Operator but not to all Operators"""
    pass


class ComponentError(Exception):
    """A component error should be fatal to a test but not the TestOperator"""


class ConnectionError(OperatorError):
    """
    A ConnectionError is raised by connections to indicate a problem.
    """
    pass
# end class ConnectionError

class ConnectionWarning(OperatorError):
    """
    A connection warning is a non-fatal connection-related error.
    """
    pass
# end class ConnectionWarning

class TimeoutError(ComponentError):
    """
    A TimeoutError is a generic Timeout exception to wrap the various timeouts
    """
    pass
# end class TimeoutError


class CommandError(ComponentError):
    """
    A CommandError reflects a problem with the command on the Device-side
    """
    pass
# end class CommandError


class StorageError(OperatorError):
    """
    An StoragError is raised by the StorageOutput
    """
    pass
# end class StorageError


class AffectorError(ComponentError):
    """
    An Affector Error is raised for non-recoverable affector errors
    """
# end class AffectorError


class ConfigurationError(OperatorError):
    """
    A ConfigurationError is raised if there is an error in the configuration file
    """
    pass
# end class ConfigurationError

class ArgumentError(OperatorError):
    """
    raised if command-line arguments don't produce valid output
    """
# end class InvocationError
