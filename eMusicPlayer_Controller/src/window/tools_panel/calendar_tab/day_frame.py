
from src.window.tools_panel.calendar_tab.day_canvas import DayCanvas

import tkinter as tk

import typing
if typing.TYPE_CHECKING:
    import src.window.tools_panel.calendar_tab.calendar_tab as calendar_tab_class


DAYS = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]


class DayFrame(tk.Frame):

    master: 'calendar_tab_class.CalendarTab'

    def __init__(self,
                 master: 'calendar_tab_class.CalendarTab',
                 day: int):

        tk.Frame.__init__(self,
                          master=master,
                          bd=-2)

        self.grid(row=0, column=day + 1, sticky=tk.NS)

        self.day = day

        self.label = tk.Label(master=self,
                              text=DAYS[self.day][:3],
                              relief=tk.GROOVE)
        self.label.pack(fill=tk.X)

        self.canvas = DayCanvas(self)

        self.label.bind('<Button-1>', lambda event: self.master.select(event, self.day))

        self.bind_all('<MouseWheel>', self.master.scroll_wheel)

        self.selected = False

    def select(self):

        self.label['bg'] = '#96C8E1'
        self.selected = True

    def deselect(self):

        self.label['bg'] = self.master.cget('bg')
        self.selected = False
