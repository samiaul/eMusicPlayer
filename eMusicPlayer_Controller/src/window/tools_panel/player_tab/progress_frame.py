
import tkinter as tk
from time import strftime, gmtime

import typing
if typing.TYPE_CHECKING:
    import src.window.tools_panel.player_tab.player_tab as player_tab_class


def format_time(value, form):

    if value is None:
        return form.replace("%H", "--").replace("%M", "--").replace("%S", "--")

    else:
        return strftime(form, gmtime(value))


class ProgressBar(tk.Frame):

    master: 'player_tab_class.PlayerTab'

    def __init__(self,
                 master: 'player_tab_class.PlayerTab'):

        tk.Frame.__init__(self,
                          master)

        self['bd'] = 2
        self['relief'] = tk.GROOVE

        self.position_label_var = tk.StringVar(self)
        self.position_label = tk.Label(self, textvariable=self.position_label_var)
        self.position_label.pack(side=tk.LEFT)

        self.position_slider_lock = False

        self.position_var = tk.IntVar(self)
        self.position_slider = tk.Scale(self,
                                        orient=tk.HORIZONTAL,
                                        showvalue=False,
                                        variable=self.position_var)
        self.position_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.position_slider.bind('<ButtonPress-1>', lambda event: self.toggle_position_slider_lock(True))

        self.bind('<ButtonRelease-1>', lambda event: self.toggle_position_slider_lock(False))

        self.duration_label_var = tk.StringVar(self)
        self.duration_label = tk.Label(self, textvariable=self.duration_label_var)
        self.duration_label.pack(side=tk.LEFT)

        self.set_position()
        self.set_duration()

        self.pack(anchor=tk.NW, fill=tk.X)

    def toggle_position_slider_lock(self, state):

        if state:
            self.position_slider_lock = True

        else:
            self.position_slider_lock = False

    def set_position(self, duration=None):

        if not self.position_slider_lock:

            self.position_label_var.set(format_time(duration, "%M:%S"))
            self.position_var.set(duration if duration is not None else 0)

    def set_duration(self, length=None):

        self.duration_label_var.set(format_time(length, "%M:%S"))
        self.position_slider['to'] = length if length is not None else 0
        self.position_var.set(0)

