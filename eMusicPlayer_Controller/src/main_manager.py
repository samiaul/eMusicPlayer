
from lib.managers.main import Main

from src.window.window_manager import WindowManager


class MainManager(Main):

    __doc__ = """
    Main management class
    """

    debug = False

    def __init__(self):

        Main.__init__(self)

        self.window_manager: WindowManager = self.add_manager(WindowManager)

    def log(self, string, is_error=False, *args, **kwargs):

        print(f"{'[ERROR] ' if is_error else ''}{string}")

    def log_error(self, error: Exception):

        self.log(error, is_error=True)

    def exit(self):
        self.log('Exiting application')
        Main.exit(self)
