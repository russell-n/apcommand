
# python standard library
import logging


DOT_JOIN = "{0}.{1}"


class BaseClass(object):
    """
    This class holds the minimum common features.
    """
    def __init__(self):        
        self._logger = None
        return

    @property
    def logger(self):
        """
        :return: A logging object.
        """
        if self._logger is None:
            self._logger = logging.getLogger(DOT_JOIN.format(self.__module__,
                                  self.__class__.__name__))
        return self._logger
# end BaseClass


class BaseThreadClass(BaseClass):
    """
    Extends the base-class with a run_thread method that will log tracebacks on exceptions.

    This is meant to log errors that kill threads.
    """
    def __init__(self):
        super(BaseThreadClass, self).__init__()
        self._logger = None
        return

    def run_thread(self, *args, **kwargs):
        """
        :param: Whatever self.run accepts
        :precondition: self.run method exists and is thread-safe
        """
        try:
            self.run(*args, **kwargs)
        except Exception as error:
            import traceback
            self.logger.debug(traceback.format_exc())
            self.logger.error(error)
        return

    def run(self):
        """
        This is called by the run_thread() method
        """
        raise NotImplementedError("BaseThreadClass children need to implement run()")
        return
# end BaseThreadClass
