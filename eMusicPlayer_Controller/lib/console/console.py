
from lib.managers.manager import Manager
from lib.console.parser import Parser
from lib.console.window import ConsoleWindow

import typing
if typing.TYPE_CHECKING:
    from lib.managers import main as main_manager_class


class Console(Manager):

    line_start = '>>> '
    intro = "Type ? to list commands"

    def __init__(self,
                 main_manager: 'main_manager_class.Main'):

        Manager.__init__(self, main_manager)

        self.parser = Parser(self)
        self.window = ConsoleWindow(self)

        self.prompt(self.intro)

    def output_log(self, string: str, is_error=False):
        """Output string to log"""
        self.window.log(string, is_error)
        # TODO file log

    def prompt(self, string, is_error=False, is_help=False):
        """Output string to console"""
        self.window.prompt(string, is_error, is_help)

    def query(self):
        """Get next string in command queue if any, else None"""
        return self.window.query()

    def update(self):

        self.window.update()
        self.parser.update()

    def stop(self):
        pass

    def quit(self):

        self.window.quit()