
import typing
if typing.TYPE_CHECKING:
    from lib.managers import main as main_manager_class


class Manager:

    __doc__ = """
    A parent class for managers
    """

    def __init__(self,
                 main_manager: 'main_manager_class.Main'):

        self.main_manager = main_manager

    def load(self):
        """Called when every manager have been initialized"""

    def update(self):
        """Called every tick"""

    def quit(self):
        pass

    def log(self, string, *args, **kwargs):

        self.main_manager.log(f"[{self.__class__.__name__}] {string}", *args, **kwargs)
