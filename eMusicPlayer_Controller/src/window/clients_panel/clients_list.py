
from src.window.clients_panel.client_box import ClientBox

import tkinter as tk

import typing
if typing.TYPE_CHECKING:
    import src.window.clients_panel as clients_panel_class


class ClientsList(tk.Frame):

    bg_color = "#BFBFBF"

    master: 'clients_panel_class.ClientsPanel'

    def __init__(self,
                 master: 'clients_panel_class.ClientsPanel'):

        tk.Frame.__init__(self,
                          master,
                          relief=tk.SUNKEN,
                          bd=2,
                          bg=self.bg_color)

        self.pack(anchor=tk.NW, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.canvas = tk.Canvas(self,
                                highlightthickness=0,
                                bg=self.bg_color)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self,
                                      orient="vertical",
                                      command=self.canvas.yview)

        self.scrollbar.pack(side=tk.RIGHT,
                            fill=tk.Y)

        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.list_frame = tk.Frame(self, relief=tk.FLAT)
        self.list_frame_id = self.canvas.create_window(0,
                                                       0,
                                                       window=self.list_frame,
                                                       anchor=tk.NW)

        self.client_boxes: typing.List['ClientBox'] = list()

        self.list_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind('<Configure>', self.update_width)

    def update_width(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.list_frame_id, width=canvas_width)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def add_client(self, client_name):

        self.client_boxes.append(ClientBox(self, client_name))
