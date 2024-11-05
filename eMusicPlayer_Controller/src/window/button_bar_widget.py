import typing

from src.window import get_state, get_icon

import tkinter as tk
import tkinter.ttk as ttk
from idlelib.tooltip import Hovertip


class ButtonBarWidget(tk.Frame):

    def __init__(self,
                 master,
                 **kwargs):

        tk.Frame.__init__(self,
                          master=master,
                          **kwargs)

        self.buttons: typing.Dict[str, typing.Union[tk.Button, tk.Checkbutton, tk.Radiobutton]] = dict()
        self.vars: typing.Dict[str, typing.Union[tk.BooleanVar, tk.IntVar]] = dict()

    def set_all_state(self,
                      state: bool):

        for button in self.buttons.values():
            button['state'] = get_state(state=state)

    def set_button_state(self,
                         name: str,
                         state: bool):

        self.buttons[name]['state'] = get_state(state=state)

    def get_var(self,
                name: str):

        return self.vars[name].get()

    def set_var(self,
                name: str,
                value):

        self.vars[name].set(value)

    def add_button(self,
                   name: str,
                   text: str,
                   command: typing.Callable = None,
                   state=True,
                   icon: typing.Union[str, bool] = None,
                   icon_factor=8,
                   pack_side: typing.Literal["left", "right", "top", "bottom"] = tk.LEFT):

        button = tk.Button(master=self,
                           image=get_icon(self, name, icon, icon_factor),
                           relief=tk.FLAT,
                           command=command,
                           state=get_state(state))

        button.pack(side=pack_side)

        Hovertip(anchor_widget=button,
                 text=str(text),
                 hover_delay=500)

        self.buttons[name] = button

    def add_checkbutton(self,
                        name: str,
                        text: str,
                        command: typing.Callable = None,
                        state=True,
                        icon: typing.Union[str, bool] = None,
                        icon_factor=8,
                        pack_side: typing.Literal["left", "right", "top", "bottom"] = tk.LEFT):

        self.vars[name] = tk.BooleanVar(self)

        button = tk.Checkbutton(master=self,
                                image=get_icon(self, name, icon, icon_factor),
                                indicatoron=False,
                                offrelief=tk.FLAT,
                                onvalue=True,
                                offvalue=False,
                                command=command,
                                variable=self.vars[name],
                                state=get_state(state))

        button.pack(side=pack_side)

        Hovertip(anchor_widget=button,
                 text=str(text),
                 hover_delay=500)

        self.buttons[name] = button

    def add_radiobutton(self,
                        name: str,
                        text: str,
                        value,
                        command: typing.Callable = None,
                        variable: str = None,
                        state=True,
                        icon: typing.Union[str, bool] = None,
                        icon_factor=8,
                        pack_side: typing.Literal["left", "right", "top", "bottom"] = tk.LEFT):

        if variable not in self.vars:
            self.vars[variable] = tk.IntVar(self)

        button = tk.Radiobutton(master=self,
                                image=get_icon(self, name, icon, icon_factor),
                                value=value,
                                offrelief=tk.FLAT,
                                variable=self.vars[variable],
                                command=command,
                                state=get_state(state),
                                indicatoron=False)

        button.pack(side=pack_side)

        Hovertip(anchor_widget=button,
                 text=str(text),
                 hover_delay=500)

        self.buttons[name] = button

    def add_separator(self):

        separator = ttk.Separator(self, orient='vertical')

        separator.pack(fill=tk.Y, side=tk.LEFT)
