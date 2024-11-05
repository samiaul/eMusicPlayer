
from src.window.button_bar_widget import ButtonBarWidget

import tkinter as tk

import typing
if typing.TYPE_CHECKING:
    import src.window.tools_panel.exceptions_tab.exceptions_tab as exceptions_tab_class


class ExceptionsToolBar(ButtonBarWidget):

    master: 'exceptions_tab_class.ExceptionsTab'

    def __init__(self,
                 master: 'exceptions_tab_class.ExceptionsTab'):

        ButtonBarWidget.__init__(self,
                                 master,
                                 bd=2,
                                 relief=tk.RIDGE)

        self.grid(row=0, column=0, sticky=tk.EW, padx=2, pady=2)

        self.add_button(name='add',
                        text="Add",
                        command=self.master.exceptions_list.add,
                        state=True)

        self.add_button(name='delete',
                        text="Delete",
                        command=self.master.exceptions_list.delete,
                        do_update=False)

        self.add_button(name='edit',
                        text="Edit",
                        command=self.master.exceptions_list.edit,
                        do_update=False)

        self.add_button(name='duplicate',
                        text="Duplicate",
                        command=self.master.exceptions_list.duplicate,
                        do_update=False)

        self.add_button(name='remove_past',
                        text="Remove Past",
                        command=self.master.exceptions_list.remove_past,
                        state=True)

    def add_button(self,
                   name: str,
                   text: str,
                   command: typing.Callable = None,
                   state=False,
                   *args,
                   **kwargs):

        ButtonBarWidget.add_button(self,
                                   name=name,
                                   text=text,
                                   command=command,
                                   state=state,
                                   icon_factor=12)
