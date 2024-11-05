
import tkinter as tk

import typing
if typing.TYPE_CHECKING:
    import src.window.clients_panel as clients_panel_class


class ToolBar(tk.Frame):

    master: 'clients_panel_class.ClientsPanel'

    def __init__(self,
                 master: 'clients_panel_class.ClientsPanel'):

        tk.Frame.__init__(self,
                          master,
                          relief=tk.RAISED,
                          bd=2)

        self.pack(anchor=tk.NE, fill=tk.X)

        tk.Button(self, text='Button_1', relief=tk.FLAT).pack(side=tk.LEFT)
        tk.Button(self, text='Button_2', relief=tk.FLAT).pack(side=tk.LEFT)
        tk.Button(self, text='Button_3', relief=tk.FLAT).pack(side=tk.LEFT)