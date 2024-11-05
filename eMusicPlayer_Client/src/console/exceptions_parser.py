
from lib.console.manager_parser import ManagerParser
from lib.console import type_parser

import typing
if typing.TYPE_CHECKING:
    from lib.console import parser as parser_class


class ExceptionsParser(ManagerParser):

    name = 'exceptions'
    doc = "Controls the schedule exceptions"

    def __init__(self,
                 parser: 'parser_class.Parser'):

        ManagerParser.__init__(self,
                               parser)

    def cmd_get_next(self):
        """Tell next exception if any"""

        ex = self.parser.console_manager.main_manager.schedule_manager.get_next_exception()

        if ex is None:
            self.parser.console_manager.prompt("No exception to come.")

        else:

            self.parser.console_manager.prompt(
                f"Next exception is: " + ex.prompt())

    @type_parser.set_args(year=type_parser.Integer(),
                          month=type_parser.Integer(),
                          day=type_parser.Integer(),
                          start_hour=type_parser.RangedInteger(0, 23),
                          start_quarter=type_parser.RangedInteger(0, 3),
                          end_hour=type_parser.RangedInteger(0, 23),
                          end_quarter=type_parser.RangedInteger(0, 3),
                          state=type_parser.Boolean(),
                          object_=type_parser.String(),
                          )
    def cmd_add(self,
                year: int,
                month: int,
                day: int,
                start_hour: int,
                start_quarter: int,
                end_hour: int,
                end_quarter: int,
                action: str,
                object_: bool):
        """Add a new exception"""
        print(year, month, day, start_hour, start_quarter, end_hour, end_quarter, action, object_)
