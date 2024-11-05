
from src.window.button_bar_widget import ButtonBarWidget

import tkinter as tk

import typing
if typing.TYPE_CHECKING:
    import src.window.tools_panel.calendar_tab.calendar_tab as calendar_tab_class


class CalendarToolBar(ButtonBarWidget):

    master: 'calendar_tab_class.CalendarTab'

    def __init__(self,
                 master: 'calendar_tab_class.CalendarTab'):

        ButtonBarWidget.__init__(self,
                                 master=master,
                                 bd=2,
                                 relief=tk.RIDGE)

        self.grid(row=1, column=0, columnspan=8, sticky=tk.EW)

        self.add_button(name='paste',
                        text='Paste',
                        command=self.master.paste,
                        state=False)

        self.add_button(name='copy',
                        text='Copy',
                        command=self.master.copy)

        self.add_button(name='night',
                        text='Night',
                        command=self.master.night)

        self.add_button(name='day',
                        text='Day',
                        command=self.master.day)

        self.add_button(name='invert',
                        text='Invert',
                        command=self.master.invert)

        self.add_button(name='clear',
                        text='Clear',
                        command=self.master.clear)

    def add_button(self,
                   name: str,
                   text: str,
                   command: typing.Callable = None,
                   state=True,
                   *args,
                   **kwargs):

        ButtonBarWidget.add_button(self,
                                   name=name,
                                   text=text,
                                   command=command,
                                   state=state)
