
#python libraries
import random
from string import ascii_letters, digits
from itertools import repeat

# arachne libraries
from apcommand.baseclass import BaseClass


EMPTY_STRING = ''


class ChangePrompt(BaseClass):
    """
    Changes a prompt.
    """
    def __init__(self, adapter, length=10, variable="PS1", prompt=None):
        """
        ChangePrompt Constructor
        
        :param:

         - `adapter`: The connection adapter for the device (needs exec_command)
         - `length`: The number of characters to use for the prompt.
         - `variable`: The name of the prompt variable on the device.
         - `prompt`: A prompt to use [default is a random one].
        """
        super(ChangePrompt, self).__init__()
        self.adapter = adapter
        self.length = length
        self.variable = variable
        self._prompt = prompt
        return

    @property
    def prompt(self):
        """
        The prompt string (random ascii if not set at construction)
        
        :return: the alternative prompt to use
        """
        if self._prompt is None:
            source = ascii_letters + digits
            self._prompt = (random.choice(ascii_letters) +
                            EMPTY_STRING.join((random.choice(source)) for x in repeat(None,
                                                                                      self.length - 1)))
        return self._prompt


    def run(self):
        """
        Sets the prompt variable to the prompt string
        
        :postcondition: prompt variable is set to new prompt.
        :return: The new prompt value.
        """
        self.adapter.prompt=self.prompt
        self.adapter.exec_command("{0}={1}".format(self.variable, self.prompt))
        return self.prompt       
# end class ChangePrompt
