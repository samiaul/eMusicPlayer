
import tkinter as tk

import typing
if typing.TYPE_CHECKING:
    import src.window.clients_panel.clients_list as clients_list_class


class ClientBox(tk.Frame):

    master: 'clients_list_class.ClientsList'

    def __init__(self,
                 master: 'clients_list_class.ClientsList',
                 client_name):

        tk.Frame.__init__(self,
                          master.list_frame,
                          relief=tk.RIDGE,
                          bd=2)

        self.pack(fill=tk.X, expand=True)

        tk.Label(self, text=client_name).pack()
        tk.Label(self, text='Active').pack()