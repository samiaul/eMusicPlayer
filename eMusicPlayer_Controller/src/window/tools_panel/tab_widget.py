
from src.window import get_root

import tkinter as tk

import typing
if typing.TYPE_CHECKING:
    import src.window.tools_panel.tools_notebook as tools_notebook_class


class TabWidget(tk.Frame):

    master: 'tools_notebook_class.ToolsNotebook'

    def __init__(self,
                 master: 'tools_notebook_class.ToolsNotebook',
                 name: str,
                 icon: str,
                 **kwargs):

        tk.Frame.__init__(self,
                          master,
                          **kwargs)

        self.pack(fill=tk.BOTH, expand=True)

        self.master.add(self, text=name, image=get_root(self).get_icon(name=icon, factor=10), compound=tk.LEFT)
