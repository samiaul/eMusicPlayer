
from lib.managers.main import Main

from src.console.console_manager import ConsoleManager
from src.session.session_manager import SessionManager
from src.playlist.playlist_manager import PlaylistManager
from src.player.player_manager import PlayerManager
from src.schedule.schedule_manager import ScheduleManager
from src.clock.clock_manager import ClockManager


class MainManager(Main):

    __doc__ = """
    Main management class
    """
    debug = False

    def __init__(self):

        Main.__init__(self)

        self.console_manager: ConsoleManager = self.add_manager(ConsoleManager)
        self.session_manager: SessionManager = self.add_manager(SessionManager)
        self.playlist_manager: PlaylistManager = self.add_manager(PlaylistManager)
        self.player_manager: PlayerManager = self.add_manager(PlayerManager)
        self.schedule_manager: ScheduleManager = self.add_manager(ScheduleManager)
        self.clock_manager: ClockManager = self.add_manager(ClockManager)

    def log(self, string, is_error=False, *args, **kwargs):

        self.console_manager.output_log(string, is_error)

    def log_error(self, error: Exception):

        self.log(error, is_error=True)

    def exit(self):
        self.log('Exiting application')
        Main.exit(self)
