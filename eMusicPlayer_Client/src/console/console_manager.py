
from lib.console.console import Console

from src.console.player_parser import PlayerParser
from src.console.clock_parser import ClockParser
from src.console.calendar_parser import CalendarParser
from src.console.exceptions_parser import ExceptionsParser
from src.console.playlist_parser import PlaylistParser

import typing
if typing.TYPE_CHECKING:
    from src import main_manager as main_manager_class


class ConsoleManager(Console):

    prompt = 'User > '
    intro = "Welcome to eMusicPlayer(Client) ! Type ? to list commands"

    main_manager: 'main_manager_class.Main'

    def __init__(self,
                 main_manager: 'main_manager_class.Main'):

        Console.__init__(self, main_manager)

        self.parser.add_manager(PlayerParser)
        self.parser.add_manager(ClockParser)
        self.parser.add_manager(CalendarParser)
        self.parser.add_manager(ExceptionsParser)
        self.parser.add_manager(PlaylistParser)

    def stop(self):
        self.main_manager.stop()

    def quit(self):

        self.log("Quitting...")