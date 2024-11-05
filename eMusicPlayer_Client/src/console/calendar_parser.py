
from lib.console.manager_parser import ManagerParser
from lib.console import type_parser

import typing
if typing.TYPE_CHECKING:
    pass


class CalendarParser(ManagerParser):

    name = 'calendar'
    doc = "Controls the schedule calendar"

    def __init__(self,
                 parser: 'parser_class.Parser'):

        ManagerParser.__init__(self,
                               parser)

    def cmd_clear(self):
        self.parser.console_manager.main_manager.schedule_manager.calendar.clear()

    def cmd_get_all(self):

        string = "    0   1   2   3   4   5   6 \n"

        for i in range(4*24):

            hour = i // 4
            quarter = i % 4

            def v(d):
                if self.parser.console_manager.main_manager.schedule_manager.calendar.get(d, hour, quarter):
                    return "███"
                else:
                    return "░░░"

            string += f"{str(hour)+' '[len(str(hour))-1:] if quarter == 0 else '  '} " \
                      f"{v(0)} {v(1)} {v(2)} {v(3)} {v(4)} {v(5)} {v(6)}\n"

        self.parser.console_manager.prompt(string)

    @type_parser.set_args(day=type_parser.RangedInteger(0, 6),
                          hour=type_parser.RangedInteger(0, 23),
                          quarter=type_parser.RangedInteger(0, 3))
    def cmd_get(self, day: int, hour: int, quarter: int):
        """Tell the schedule state at a specified calendar datetime"""

        self.parser.console_manager.prompt(
            self.parser.console_manager.main_manager.schedule_manager.calendar.get(day, hour, quarter))

    @type_parser.set_args(state=type_parser.Boolean(),
                          day=type_parser.RangedInteger(0, 6),
                          hour=type_parser.RangedInteger(0, 23),
                          quarter=type_parser.RangedInteger(0, 3),
                          end_hour=type_parser.RangedInteger(0, 23, None),
                          end_quarter=type_parser.RangedInteger(0, 3, None))
    def cmd_set(self,
                state: bool,
                day: int,
                hour: int,
                quarter: int,
                end_hour: int = None,
                end_quarter: int = None):
        """Set the schedule state at a specified calendar datetime"""

        if end_hour is not None:
            if end_hour < hour:
                raise type_parser.InvalidValueException(end_hour, "end hour lower than hour")

            elif end_hour == hour:
                if end_quarter is not None:
                    if end_quarter < quarter:
                        raise type_parser.InvalidValueException(end_quarter, "end quarter lower than quarter")

        self.parser.console_manager.main_manager.schedule_manager.calendar.set_range(
            day=day,
            hour1=hour,
            quarter1=quarter,
            hour2=end_hour,
            quarter2=end_quarter,
            state=state
        )