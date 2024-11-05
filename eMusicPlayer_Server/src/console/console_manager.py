
from lib.console.console import Console

from src.console.network_parser import NetworkParser

import typing
if typing.TYPE_CHECKING:
    from src import main_manager as main_manager_class


class ConsoleManager(Console):

    prompt = 'User > '
    intro = "Welcome to eMusicPlayer(Server) ! Type ? to list commands"

    main_manager: 'main_manager_class.Main'

    def __init__(self,
                 main_manager: 'main_manager_class.Main'):

        Console.__init__(self, main_manager)

        self.parser.add_manager(NetworkParser)

    def stop(self):
        self.main_manager.stop()

    def quit(self):

        self.log("Quitting...")