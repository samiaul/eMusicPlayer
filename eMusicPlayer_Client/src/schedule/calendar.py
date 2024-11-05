
from src.funcs import hyperlist, group

import typing
if typing.TYPE_CHECKING:
    import datetime as datetime_class

    calendarType = typing.List[typing.List[typing.Union[int, typing.Tuple[int, int]]]]


class Calendar:

    __doc__ = """
    Stores timesheet of a schedule
    """

    def __init__(self):

        self.timesheet: calendarType = hyperlist(False, 7, 24, 4)

    def get(self, day: int, hour: int, quarter: int):
        """Return the state for the corresponding day and time"""

        return self.timesheet[day][hour][quarter]

    def set(self, day: int, hour: int, quarter: int, state: bool):
        """Set the state for the corresponding day and time"""

        self.timesheet[day][hour][quarter] = state

    def set_range(self, day: int, hour1: int, quarter1: int, hour2: int, quarter2: int, state: bool):
        """Set the state in range [hour1:quarter1; hour2:quarter2[ """

        for hour in range(hour1, hour2+1):

            start_quarter = quarter1 if hour == hour1 else 0
            end_quarter = quarter2 if hour == hour2 else 4

            for quarter in range(start_quarter, end_quarter):
                self.set(day, hour, quarter, state)

    def get_at(self, datetime: 'datetime_class.datetime'):
        """Return the state at a daytime"""

        return self.get(datetime.weekday(), datetime.hour, datetime.minute//15)

    def clear(self):
        """Reset all calendar to false"""

        self.timesheet = hyperlist(False, 7, 24, 4)

    def encode(self):

        calendar: 'calendarType' = list()

        for d, day in enumerate(self.timesheet):

            if any([any([self.get(d, h, m) for m in range(4)]) for h in range(24)]):

                calendar.append([d])

                curr_state = False

                flat_day = [(hour, quarter, state)
                            for hour, quarters in enumerate(day)
                            for quarter, state in enumerate(quarters)]

                for hour, quarter, state in flat_day:

                    if state != curr_state:
                        calendar[-1].append((hour, quarter))
                        curr_state = state

        return calendar

    def decode(self, datas: 'calendarType'):

        for day_data in datas:

            d = day_data[0]

            day = day_data[1:]

            for (hour1, quarter1), (hour2, quarter2) in group(day, 2):
                self.set_range(d, hour1, quarter1, hour2, quarter2, True)
