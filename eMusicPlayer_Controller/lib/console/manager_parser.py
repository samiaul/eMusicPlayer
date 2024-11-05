
from lib.console import type_parser, parser as parser_class

import typing
if typing.TYPE_CHECKING:
    pass


class UnknownManagerCmd(ValueError):
    def __init__(self, command: str):
        self.command = command


class ManagerParser:

    name = 'generic'
    doc = ""

    def __init__(self,
                 parser: 'parser_class.Parser'):

        self.parser = parser

    def help(self, *args):

        if args:

            arg = args[0]

            try:
                doc = getattr(self, 'cmd_' + arg).__doc__
                if doc:
                    self.parser.console_manager.prompt(f"{doc}", is_help=True)
                    return
            except AttributeError:
                pass
            self.parser.console_manager.prompt(f"*** No help on {self.name} {arg}", is_help=True)

        else:
            header = f"Documented commands (type help {self.name} <topic>):"
            cmds = list(map(lambda name: name.removeprefix("cmd_"), self.get_commands()))
            self.parser.print_topics(header, cmds, 15, 80, is_help=True)

    def help_command(self, arg):
        pass

    def get_commands(self):
        return filter(lambda name: name.startswith("cmd_"), self.__class__.__dict__)

    def execute(self, *args):

        if not args:
            self.parser.console_manager.prompt(f"*** Missing command for {self.name}", is_error=True)
        else:
            command, *args = args
            self.run_command(command, *args)

    def run_command(self, command, *args):

        try:
            getattr(self, "cmd_" + command)(*args)

        except AttributeError as e:
            self.parser.console_manager.prompt(f"*** No {self.name} command: {command}", is_error=True)

        except type_parser.ParseException as error:
            self.parser.console_manager.prompt(str(error), is_error=True)
