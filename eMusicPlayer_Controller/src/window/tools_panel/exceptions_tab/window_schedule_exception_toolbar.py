
from assets.window_button_bar_type import ButtonBarType

import tkinter as tk


class ExceptionsToolBar(ButtonBarType):

    def __init__(self, master):
        ButtonBarType.__init__(self, master=master)

        self.main = master.main

        self['bd'] = 2
        self['relief'] = tk.RIDGE

        self.buttons = dict()

        self.add_button(name='add',
                        text=self.main.lang_manager.schedule.exceptions.button.add,
                        command=self.master.frame.add,
                        state=True)

        self.add_button(name='delete',
                        text=self.main.lang_manager.schedule.exceptions.button.delete,
                        command=self.master.frame.delete,
                        do_update=False)

        self.add_button(name='edit',
                        text=self.main.lang_manager.schedule.exceptions.button.edit,
                        command=self.master.frame.edit,
                        do_update=False)

        self.add_button(name='duplicate',
                        text=self.main.lang_manager.schedule.exceptions.button.duplicate,
                        command=self.master.frame.duplicate,
                        do_update=False)

        self.add_button(name='remove_past',
                        text=self.main.lang_manager.schedule.exceptions.button.remove_past,
                        command=self.master.frame.remove_past,
                        state=True)

        self.grid(row=0, column=0, sticky=tk.EW, padx=2, pady=2)

    @ButtonBarType.override
    def add_button(self,
                   name,
                   text,
                   command,
                   iocommand=None,
                   do_update=True,
                   state=False):

        ButtonBarType.add_button(self,
                                 name=name,
                                 text=text,
                                 command=command,
                                 state=state,
                                 iocommand=iocommand,
                                 do_update=do_update,
                                 image_factor=12)
