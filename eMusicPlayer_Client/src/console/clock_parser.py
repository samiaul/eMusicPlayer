
from lib.console.manager_parser import ManagerParser
from lib.console import type_parser

import typing
if typing.TYPE_CHECKING:
    pass


class ClockParser(ManagerParser):

    name = 'clock'
    doc = "Controls the clock"

    def __init__(self,
                 parser: 'parser_class.Parser'):

        ManagerParser.__init__(self,
                               parser)

    @type_parser.set_args(state=type_parser.Boolean())
    def cmd_set_pause(self, state):
        """Set the state of the clock. If false, it won't check for auto-play"""
        self.parser.console_manager.main_manager.clock_manager.set_pause_state(state)

    def cmd_now(self):
        self.parser.console_manager.prompt(
            self.parser.console_manager.main_manager.clock_manager.get_now().isoformat(sep=' ', timespec='milliseconds'))