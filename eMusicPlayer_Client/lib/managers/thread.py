
from lib.managers.manager import Manager

import threading

import typing
if typing.TYPE_CHECKING:
    from lib.managers import main as main_manager_class


class Thread(threading.Thread, Manager):

    __doc__ = """
    A parent class for threaded managers
    """

    def __init__(self,
                 main_manager: 'main_manager_class.Main'):

        threading.Thread.__init__(self)
        Manager.__init__(self, main_manager)

        self.thread_state = None

        self.executions: typing.List[typing.Tuple[str, typing.Tuple, typing.Dict]] = list()

    def run(self):
        """Start the thread"""

        self.thread_state = True

        self.loop()

    def loop(self):
        """Call update function while state is True, then call quit"""

        while self.thread_state:
            self.main_manager.update_manager(self)

        self.quit()

    def update(self):
        """Executed once every loop"""

        Manager.update(self)

        self.run_executions()

    def execute(self, method, *args, **kwargs):
        """Set a method to be executed in thread loop"""

        self.executions.append((method, args, kwargs))

    def run_executions(self):

        for method, args, kwargs in self.executions:
            getattr(self, method)(*args, **kwargs)

        self.executions.clear()

    def stop(self):
        """Set the thread to stop"""

        self.thread_state = False

    def quit(self):
        """Execute after last loop"""
        pass
