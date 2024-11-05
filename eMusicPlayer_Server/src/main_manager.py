
from lib.managers.main import Main

from src.console.console_manager import ConsoleManager
from src.network.network_manager import NetworkManager


class MainManager(Main):

    __doc__ = """
    Main management class
    """
    debug = False

    def __init__(self):

        Main.__init__(self)

        self.console_manager: ConsoleManager = self.add_manager(ConsoleManager)
        self.session_manager: NetworkManager = self.add_manager(NetworkManager)

    def log(self, string, is_error=False, *args, **kwargs):

        self.console_manager.output_log(string, is_error)

    def log_error(self, error: Exception):

        self.log(error, is_error=True)

    def exit(self):
        self.log('Exiting application')
        Main.exit(self)
