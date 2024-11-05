
from src.window.tools_panel.tools_notebook import ToolsNotebook

import tkinter as tk


import typing
if typing.TYPE_CHECKING:
    import src.window.window_manager as window_manager_class


class ToolsPanel(tk.Frame):

    master: 'window_manager_class.WindowManager'

    def __init__(self,
                 master: 'window_manager_class.WindowManager'):

        tk.Frame.__init__(self, master)

        self['relief'] = tk.SUNKEN
        self['bd'] = 2

        self.notebook = ToolsNotebook(self)

        self.grid(column=1, row=0, sticky=tk.NSEW)