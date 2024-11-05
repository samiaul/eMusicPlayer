
import tkinter as tk
from datetime import datetime

import typing
if typing.TYPE_CHECKING:
    from lib.console import console as console_class


def index_range(value, minimum, maximum):

    value_l, value_c = value.split('.')
    min_l, min_c = minimum.split('.')
    max_l, max_c = maximum.split('.')

    return (int(value_l) in range(int(min_l), int(max_l)+1) and
            int(value_c) in range(int(min_c), int(max_c)+1))


class ConsoleWindow(tk.Tk):

    def __init__(self,
                 console_manager: 'console_class.Console'):

        tk.Tk.__init__(self)

        self.console_manager = console_manager

        self.title(f"console")
        self.protocol('WM_DELETE_WINDOW', lambda: self.console_manager.stop())

        self.state = True

        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.log_frame = LogFrame(self)
        self.console_frame = ConsoleFrame(self)

    def update(self):

        self.log_frame.update()
        self.console_frame.update()

        tk.Tk.update(self)
        tk.Tk.update_idletasks(self)

    def quit(self):

        tk.Tk.destroy(self)

        self.state = False

    def log(self, string, is_error=False):
        """Display string to log frame"""
        self.log_frame.prompt(string, is_error)

    def prompt(self, string, is_error=False, is_help=False):
        """Display string to console frame"""
        self.console_frame.prompt(string, is_error, is_help)

    def query(self):
        """Get next string in command queue if any, else None"""
        return self.console_frame.query()


class LineFrame(tk.Frame):

    def __init__(self, master):

        tk.Frame.__init__(self, master, bd=0, bg='white')

        self.text = tk.Text(self, bd=0, bg='black', fg='white', insertbackground='white')
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=1, pady=1)

        self.scrollbar = tk.Scrollbar(self, bd=0)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH, padx=1, pady=1)

        self.text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text.yview)

        self.prompt_queue = list()

    def prompt(self, string, *args):
        """Set a string to be displayed"""

        self.prompt_queue.append((string, *args))

    def update(self):
        """Display next string in prompt queue, if any"""

        if self.prompt_queue:
            string, *args = self.prompt_queue.pop(0)
            lines = string.split('\n')
            for line in lines:
                self.write(line, *args)

    def write(self, string, *args):
        """Display string on next line"""
        pass


class LogFrame(LineFrame):

    def __init__(self, master):
        """A frame with read-only text"""

        LineFrame.__init__(self, master)

        self.text['state'] = tk.DISABLED

        self.text.tag_config("error", foreground="red")

        self.grid(row=0, sticky="nsew")

    def write(self, string, is_error=False):

        time = datetime.now().strftime("[%H:%M:%S] ")

        self.text['state'] = tk.NORMAL
        self.text.insert(tk.END, time + string + '\n')
        self.text['state'] = tk.DISABLED

        if is_error:
            self.text.tag_add("error", "end-2l", "end-2l lineend")

        if self.scrollbar.get()[1] == 1:
            self.text.yview_moveto(1)


class ConsoleFrame(LineFrame):

    master: 'ConsoleWindow'

    def __init__(self, master):
        """A frame with editable text widget
        Press 'return' to submit a command to parse"""

        LineFrame.__init__(self, master)

        self.text.insert(tk.END, self.master.console_manager.line_start)

        self.grid(row=1, sticky="nsew")

        self.text.bind('<Return>', self.submit)
        self.text.bind('<Key>', self.reset_cursor)
        self.text.bind('<ButtonRelease-1>', self.reset_cursor)

        self.text.tag_config("error", foreground="red")
        self.text.tag_config("help", foreground="green")

        self.cmd_queue = list()
        self.prompt_queue = list()

    def submit(self, *args):
        """Called when return key is pressed
        Set a string to be parsed"""

        string = self.text.get("end-1l", "end-1l lineend")

        self.text.delete("end-1l + %sc" % len(self.master.console_manager.line_start),
                         "end-1l + %sc lineend" % len(self.master.console_manager.line_start))

        self.write(string)

        self.cmd_queue.append(string)

        return "break"

    def query(self):
        """Get next string in command queue if any, else None"""

        if self.cmd_queue:
            return self.cmd_queue.pop(0)
        else:
            return None

    def write(self, string, is_error=False, is_help=False):

        self.text.insert("end-1l", f"{string}\n")

        if is_error:
            self.text.tag_add("error", "end-2l", "end-2l lineend")
        elif is_help:
            self.text.tag_add("help", "end-2l", "end-2l lineend")

        self.text.mark_set("insert", "end+1c")

    def reset_cursor(self, event):
        """Reset cursor pos to last character"""

        is_in_range = index_range(self.text.index("insert"),
                                  self.text.index("end-1l + %sc" % (len(self.master.console_manager.line_start)+1)),
                                  self.text.index("end-1l lineend"))

        self.text.mark_set("insert", "end+1c")

        if event.keysym == 'BackSpace' and not is_in_range:
            return "break"
