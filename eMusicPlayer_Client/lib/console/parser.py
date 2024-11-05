
from string import ascii_letters, digits

import typing
if typing.TYPE_CHECKING:
    from lib.console import console as console_class
    from lib.console import manager_parser as manager_parser_class


def split(string):

    i = -1
    is_string = False

    word = ''
    words = []

    while i < len(string)-1:

        i += 1

        char = string[i]

        if char == ' ':

            if is_string:
                word += char

            elif word:
                words.append(word)
                word = ''

        elif char == '"':

            if is_string:
                words.append(word)
                word = ''
                is_string = False

            else:
                is_string = True

        else:
            word += char

    if word:
        words.append(word)

    return words


class Parser:

    identchars = ascii_letters + digits + '_'

    def __init__(self,
                 console_manager: 'console_class.Console'):

        self.console_manager = console_manager

        self.last_cmd = ''

    def add_manager(self,
                    manager_class: typing.Type['manager_parser_class.ManagerParser']):

        instance = manager_class(self)

        def method(*args):

            instance.execute(*args)

        setattr(self, f"do_{instance.name}", method)
        setattr(self, f"help_{instance.name}", instance.help)

    def update(self):

        line = self.console_manager.query()

        if line is not None:

            cmd, args, line = self.parseline(line)

            self.execute(cmd, args, line)

    def execute(self, cmd, args, line):
        """Interpret the argument as though it had been typed in response
        to the prompt"""

        if not line:
            self.emptyline()
            return

        if cmd is None:
            self.default(line)
            return

        self.last_cmd = line

        if line == 'EOF':
            self.last_cmd = ''

        if cmd == '':
            self.default(line)

        else:

            try:
                func = getattr(self, f"do_{cmd}")
            except AttributeError:
                self.default(line)
            else:
                func(*args)

    def parseline(self, line):
        """Parse the line into a command name and a string containing
        the arguments.  Returns a tuple containing (command, args, line).
        'command' and 'args' may be None if the line couldn't be parsed.
        """

        line = line.removeprefix(self.console_manager.line_start)

        line = line.strip()

        if not line:
            return None, (), line

        elif line[0] == '?':
            line = f"help {line[1:]}".strip()

        cmd, *args = split(line)

        return cmd, args, line

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.
        Repeats the last nonempty command entered."""

        if self.last_cmd:

            cmd, args, line = self.parseline(self.last_cmd)

            self.execute(cmd, args, line)

        else:
            self.default(self.last_cmd)

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.
        Prints an error message"""
        self.console_manager.prompt(f"*** Unknown syntax: {line}", is_error=True)

    def print_topics(self, header, cmds, cmdlen, maxcol, is_help=False):

        if cmds:
            self.console_manager.prompt(f"{header}", is_help=is_help)
            self.console_manager.prompt(f"{'=' * len(header)}", is_help=is_help)
            self.columnize(cmds, maxcol-1, is_help=is_help)

    def columnize(self, list_, displaywidth=80, is_help=False):
        """Display a list of strings as a compact set of columns.

        Each column is only as wide as necessary.
        Columns are separated by two spaces (one was not legible enough).
        """
        if not list_:
            self.console_manager.prompt("<empty>", is_help=is_help)
            return

        nonstrings = [i for i in range(len(list_))
                      if not isinstance(list_[i], str)]
        if nonstrings:
            raise TypeError(f"list[i] not a string for i in {', '.join(map(str, nonstrings))}")
        size = len(list_)
        if size == 1:
            self.console_manager.prompt(f"{str(list_[0])}", is_help=is_help)
            return
        # Try every row count from 1 upwards
        for nrows in range(1, len(list_)):
            ncols = (size+nrows-1) // nrows
            colwidths = []
            totwidth = -2
            for col in range(ncols):
                colwidth = 0
                for row in range(nrows):
                    i = row + nrows*col
                    if i >= size:
                        break
                    x = list_[i]
                    colwidth = max(colwidth, len(x))
                colwidths.append(colwidth)
                totwidth += colwidth + 2
                if totwidth > displaywidth:
                    break
            if totwidth <= displaywidth:
                break
        else:
            nrows = len(list_)
            ncols = 1
            colwidths = [0]
        for row in range(nrows):
            texts = []
            for col in range(ncols):
                i = row + nrows*col
                if i >= size:
                    x = ""
                else:
                    x = list_[i]
                texts.append(x)
            while texts and not texts[-1]:
                del texts[-1]
            for col in range(len(texts)):
                texts[col] = texts[col].ljust(colwidths[col])
            self.console_manager.prompt(f"{str('  '.join(texts))}", is_help=is_help)

    # -- CONSOLE COMMANDS --

    def do_exit(self, *args):
        """Exit the application. Shorthand: Ctrl-D."""
        self.console_manager.prompt("Bye")
        self.console_manager.main_manager.stop()

    def do_help(self, *args):
        """List available commands with "help" or detailed help with "help cmd"."""

        if args:

            command, *args = args

            try:
                func = getattr(self, f"help_{command}")

            except AttributeError:

                try:
                    doc = getattr(self, f"do_{command}").__doc__

                    if doc:
                        self.console_manager.prompt(doc, is_help=True)
                        return

                except AttributeError:
                    pass

                self.console_manager.prompt(f"*** No help on {command}", is_help=True)
                return

            func(*args)

        else:

            names = list(self.__dict__.keys()) + list(self.__class__.__dict__.keys())
            cmds = list()
            help = {}

            for name in names:
                if name[:5] == 'help_':
                    help[name[5:]] = 1

            names.sort()
            prevname = ''

            for name in names:
                if name[:3] == 'do_':
                    if name == prevname:
                        continue
                    prevname = name
                    cmd = name[3:]
                    if cmd in help:
                        cmds.append(cmd)
                        del help[cmd]
                    elif getattr(self, name).__doc__:
                        cmds.append(cmd)

            self.print_topics("Documented commands (type help <topic>):", cmds, 15, 80, is_help=True)

    do_EOF = do_exit