
from lib.managers.manager import Manager

from src.window.menu_bar import MenuBar
from src.window.clients_panel import ClientsPanel
from src.window.tools_panel import ToolsPanel

import tkinter as tk

import typing
if typing.TYPE_CHECKING:
    import src.main_manager as main_manager_class


class WindowManager(tk.Tk, Manager):

    def __init__(self,
                 main_manager: 'main_manager_class.MainManager'):

        tk.Tk.__init__(self)
        Manager.__init__(self, main_manager)

        self.title(f"eMusicPlayer [Control Panel]")
        self.iconbitmap(default='icon.ico')

        self.protocol('WM_DELETE_WINDOW', lambda: self.main_manager.stop())

        self.geometry("1280x720")

        self.option_add('*tearOff', False)

        self.icons = []
        #self.icons_files = decompress_files("icons")
        self.links = list()

        #self.dialogs = Dialogs
        #self.dialogs.root = self

        self.menu_bar = MenuBar(self)
        self.clients_panel = ClientsPanel(self)
        self.tools_panel = ToolsPanel(self)

        #self.settings_window = None

        self.grid_columnconfigure(index=0, weight=5)
        self.grid_columnconfigure(index=1, weight=3)

        self.grid_rowconfigure(index=0, weight=1)

    def get_icon(self, name, factor=8):
        self.icons.append(tk.PhotoImage(master=self,
                                        file=f"icons/{name}.png").subsample(x=factor,
                                                                            y=factor))

        return self.icons[-1]

    """
    def get_icon(self, name, factor=8):
        self.icons.append(tk.PhotoImage(master=self,
                                        data=self.icons_files[name].read()).subsample(x=factor,
                                                                                      y=factor))

        return self.icons[-1]
    """

    #def open_settings(self):
        #self.settings_window = SettingsWindow(self)

    def quit(self):

        self.destroy()

    def update(self):

        tk.Tk.update(self)
        tk.Tk.update_idletasks(self)
