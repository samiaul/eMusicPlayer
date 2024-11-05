
from lib.console.manager_parser import ManagerParser

import typing
if typing.TYPE_CHECKING:
    from lib.console import parser as parser_class


class PlayerParser(ManagerParser):

    name = 'player'
    doc = "Controls the music player"

    def __init__(self,
                 parser: 'parser_class.Parser'):

        ManagerParser.__init__(self,
                               parser)

    def test_lock(self):

        if not self.parser.console_manager.main_manager.clock_manager.pause_state:
            self.parser.console_manager.prompt("*** Can't use player while clock is not paused", is_error=True)
            return False
        return True

    def cmd_play(self):
        """Start music streaming"""

        if self.test_lock():
            self.parser.console_manager.main_manager.player_manager.execute('play_music')

    def cmd_stop(self):
        """Stop music streaming"""

        if self.test_lock():
            self.parser.console_manager.main_manager.player_manager.execute('stop_music')

    def cmd_pause(self):
        """Pause music streaming"""

        if self.test_lock():
            self.parser.console_manager.main_manager.player_manager.execute('pause_music')

    def cmd_next(self):
        """Play next music in playlist"""

        if self.test_lock():
            self.parser.console_manager.main_manager.player_manager.execute('next_music')

    def cmd_previous(self):
        """Play last music in playlist"""

        if self.test_lock():
            self.parser.console_manager.main_manager.player_manager.execute('previous_music')

    def cmd_get_pause_state(self):
        """Tell if music streaming is paused"""

        self.parser.console_manager.prompt(
            f"player pause_state = {self.parser.console_manager.main_manager.player_manager.pause_state}")

    def cmd_get_play_state(self):
        """Tell if music streaming is not stopped"""

        self.parser.console_manager.prompt(
            f"player play_state = {self.parser.console_manager.main_manager.player_manager.pause_state}")
