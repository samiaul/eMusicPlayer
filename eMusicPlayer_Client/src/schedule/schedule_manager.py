
from lib.managers.manager import Manager

from src.schedule.calendar import Calendar
from src.schedule.exception import ScheduleException

import typing
if typing.TYPE_CHECKING:
    from src import main_manager as main_manager_class

    from src.schedule.exception import ExceptionTuple


class ScheduleManager(Manager):

    __doc__ = """
    Manage schedule datas :
        - Schedules
        - Exceptions
        - Adverts
        - Top-Of-The-Hours
    """

    main_manager: 'main_manager_class.MainManager'

    def __init__(self,
                 main_manager: 'main_manager_class.Main'):

        Manager.__init__(self, main_manager)

        self.calendar = Calendar()

        self.exceptions: typing.List['ScheduleException'] = list()

    def decode_exceptions(self, datas: typing.List['ExceptionTuple']):

        for exception_datas in datas:
            self.exceptions.append(ScheduleException(self, exception_datas))

    def encode_exceptions(self):

        return [ex.get_values() for ex in self.exceptions]

    def get_next_exception(self):

        candidate = None
        for exception in self.exceptions:

            if (
                    candidate is None or
                    (
                    not exception.is_passed() and
                    not exception.is_current() and
                    exception.get_start_daytime() < candidate.get_start_daytime()
                    )
            ):
                candidate = exception

        return candidate

    def get_current_exception(self):

        for exception in self.exceptions:
            if exception.is_current():
                return exception

    def quit(self):

        self.log("Quitting...")