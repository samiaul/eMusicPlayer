
from lib.managers.thread import Thread

import typing
if typing.TYPE_CHECKING:
    import lib.managers.manager as manager_class


class ManagerError(Exception):

    def __init__(self, msg: str, manager: str, error: Exception):

        self.msg = msg
        self.manager = manager
        self.error = error

        Exception.__init__(self, f"{msg.format(manager=manager)}: {error}")


class ManagerInitError(ManagerError):

    def __init__(self, manager: str, error: Exception):
        ManagerError.__init__(self,
                              "Couldn't initialize '{manager}'",
                              manager,
                              error)


class ManagerLoadError(ManagerError):

    def __init__(self, manager: str, error: Exception):
        ManagerError.__init__(self,
                              "Couldn't load '{manager}'",
                              manager,
                              error)


class ManagerStartError(ManagerError):

    def __init__(self, manager: str, error: Exception):
        ManagerError.__init__(self,
                              "Couldn't start thread '{manager}'",
                              manager,
                              error)


class ManagerUpdateError(ManagerError):

    def __init__(self, manager: str, error: Exception):
        ManagerError.__init__(self,
                              "Exception while updating '{manager}'",
                              manager,
                              error)


class ManagerJoinError(ManagerError):

    def __init__(self, manager: str, error: Exception):
        ManagerError.__init__(self,
                              "Couldn't join thread '{manager}'",
                              manager,
                              error)


class ManagerQuitError(ManagerError):

    def __init__(self, manager: str, error: Exception):
        ManagerError.__init__(self,
                              "Couldn't properly exit '{manager}'",
                              manager,
                              error)


class Main:

    # If true: Manager exception aren't caught, terminating the program
    # If False: The program try to continue running and send any exception to log
    debug = False

    def __init__(self):

        self.state = None

        self.managers = list()

    def debug_catcher(self, exception):

        if self.debug:

            self.log_error(exception)

        else:
            raise exception

    def add_manager(self, manager: typing.Type['manager_class.Manager']):
        """Try adding a new manager"""

        try:
            instance = manager(self)

        except Exception as error:
            self.debug_catcher(ManagerInitError(manager.__name__, error))

        else:
            self.managers.append(instance)
            return instance

    def load_manager(self, manager: 'manager_class.Manager'):
        """Try loading a manager"""

        try:
            manager.load()

        except Exception as error:
            self.debug_catcher(ManagerLoadError(manager.__class__.__name__, error))

    def update_manager(self, manager: 'manager_class.Manager'):
        """Try updating a manager"""

        try:
            manager.update()

        except Exception as error:
            self.debug_catcher(ManagerUpdateError(manager.__class__.__name__, error))

    def start_manager(self, manager: Thread):
        """Try starting a manager"""

        try:
            manager.start()

        except Exception as error:
            self.debug_catcher(ManagerStartError(manager.__class__.__name__, error))

    def join_manager(self, manager: Thread):
        """Try stopping a manager"""

        try:
            manager.stop()
            manager.join()

        except Exception as error:
            self.debug_catcher(ManagerJoinError(manager.__class__.__name__, error))

    def quit_manager(self, manager: 'manager_class.Manager'):
        """Try stopping a manager"""

        try:
            manager.quit()

        except Exception as error:
            self.debug_catcher(ManagerQuitError(manager.__class__.__name__, error))

    def load(self):

        for manager in self.managers:
            manager.load()

    def run(self):

        for manager in self.managers:

            if isinstance(manager, Thread):
                self.start_manager(manager)

        self.state = True

        self.loop()

    def loop(self):

        while self.state:
            self.update()

        self.exit()

    def update(self):

        for manager in self.managers:

            if not isinstance(manager, Thread):
                self.update_manager(manager)

    def stop(self):

        self.state = False

    def exit(self):
        """Try to properly quit each manager before setting state to false"""

        for manager in self.managers[::-1]:

            if isinstance(manager, Thread):
                self.join_manager(manager)

            else:
                self.quit_manager(manager)

    def log(self, string, *args, **kwargs):

        print(f"{args} {kwargs} '{string}'")

    def log_error(self, error: Exception):

        self.log(error, 'error')
