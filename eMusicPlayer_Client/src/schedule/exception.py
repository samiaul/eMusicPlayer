
from datetime import datetime

import typing
if typing.TYPE_CHECKING:
    from src.schedule import schedule_manager as schedule_manager_class

    class ExceptionTuple(typing.NamedTuple):
        year: int
        month: int
        day: int
        start_hour: int
        start_quarter: int
        end_hour: int
        end_quarter: int
        action: bool
        object: str


class ScheduleException:

    __doc__ = """
    Stores data of an exception
    """

    def __init__(self,
                 schedule_manager: 'schedule_manager_class.ScheduleManager',
                 default: 'ExceptionTuple'):

        self.schedule_manager = schedule_manager

        self.year = None
        self.month = None
        self.day = None
        self.start_hour = None
        self.start_quarter = None
        self.end_hour = None
        self.end_quarter = None
        self.action = None
        self.object = None

        self.set_values(self.get_default() if default is None else default)

    def prompt(self):

        weekday = ("Monday, Thuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")[
            self.schedule_manager.main_manager.clock_manager.get_weekday(self.year, self.month, self.day)]
        action = 'Playing' if self.action else 'Stopping'

        return ("Exception"
                f"on {weekday} {self.year}/{self.month}/{self.day} "
                f"from {self.start_hour}:{self.start_quarter} "
                f"to {self.end_hour}:{self.end_quarter} "
                f"{action} for \"{self.object}\"")

    def get_values(self):
        """Return values as tuple"""

        return (
            self.year,
            self.month,
            self.day,
            self.start_hour,
            self.start_quarter,
            self.end_hour,
            self.end_quarter,
            self.action,
            self.object
        )

    def get_start_daytime(self):
        """Return values as daytime"""

        return datetime(year=self.year,
                        month=self.month,
                        day=self.day,
                        hour=self.start_hour,
                        minute=self.start_quarter)

    def get_end_daytime(self):
        """Return values as daytime"""

        return datetime(year=self.year,
                        month=self.month,
                        day=self.day,
                        hour=self.end_hour,
                        minute=self.end_quarter)

    def set_values(self, values: 'ExceptionTuple'):

        self.year = values[0]
        self.month = values[1]
        self.day = values[2]
        self.start_hour = values[3]
        self.start_quarter = values[4]
        self.end_hour = values[5]
        self.end_quarter = values[6]
        self.action = values[7]
        self.object = values[8]

    def get_default(self):
        """Return the default values for a new exception (soonest & shortest)"""

        now = self.schedule_manager.main_manager.clock_manager.get_now()

        return (
            now.year, now.month, now.day,
            (now.hour + int(now.minute >= 45)),  # Next hour if minutes >= 45
            ((now.minute // 15 + 1) * 15) % 60,  # Round minute to next multiple of 15|mod(60)
            (now.hour + int((now.minute + 15) >= 45)),  # Next hour if minutes >= 45
            ((now.minute // 15 + 2) * 15) % 60,  # Round minute to second next multiple of 15|mod(60)
            0,
            ""
        )

    def is_current(self):
        """Return true if the time is inside exception range"""

        now = self.schedule_manager.main_manager.clock_manager.get_now()

        return not self.is_passed() and now > self.get_start_daytime()

    def is_passed(self):
        """Return true if the time is beyond exception range"""

        now = self.schedule_manager.main_manager.clock_manager.get_now()

        return now > self.get_end_daytime()
