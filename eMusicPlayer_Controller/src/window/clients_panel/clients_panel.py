
from src.window.clients_panel.tool_bar import ToolBar
from src.window.clients_panel.clients_list import ClientsList

import tkinter as tk

import typing
if typing.TYPE_CHECKING:
    import src.window.window_manager as window_manager_class


class ClientsPanel(tk.Frame):

    master: 'window_manager_class.WindowManager'

    def __init__(self,
                 master: 'window_manager_class.WindowManager'):

        tk.Frame.__init__(self,
                          master,
                          relief=tk.SUNKEN,
                          bd=2)

        self.grid(column=0, row=0, sticky=tk.NSEW)

        self.tool_bar = ToolBar(self)
        self.clients_list = ClientsList(self)
