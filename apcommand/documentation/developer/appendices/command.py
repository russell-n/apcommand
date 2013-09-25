
import collections


class Command(object):
    """
    The Command adapts functions to the command-pattern
    """
    def __init__(self, do, undo, description=""):
        """
        Command constructor

        :param:

         - `do`: callable function
         - `undo`: callable function that un-does what do does
         - `description`: description of the command
        """
        assert isinstance(do, collections.Callable)
        assert isinstance(undo, collections.Callable)
        self.do = do
        self.undo = undo
        return

    def __call__(self):
        self.do()
        return
# end class Command    


class Macro(object):
    """
    A Macro bundles commands.
    """
    def __init__(self, description=""):
        self.description = description
        self._commands = []
        return

    def add(self, command):
        """
        :param:

         - `command`: Command implementation
        """
        if not(isinstance(command, Command)):
            raise TypeError("Expected object of type Command, got {0}".format(type(Command)))
        self._commands.append(command)
        return

    def __call__(self):
        """
        The main interface -- calls all commands
        """
        for command in self._commands:
            command()
        return

    def undo(self):
        """
        Calls commands' undos in reverse order
        """
        for command in reversed(self._commands):
            command.undo()
        return
# end class Macro    
