
from src.window.tools_panel.session_tab.session_tab import SessionTab
from src.window.tools_panel.settings_tab.settings_tab import SettingsTab
from src.window.tools_panel.player_tab.player_tab import PlayerTab
from src.window.tools_panel.playlist_tab.playlist_tab import PlaylistTab
from src.window.tools_panel.calendar_tab.calendar_tab import CalendarTab
from src.window.tools_panel.exceptions_tab.exceptions_tab import ExceptionsTab
from src.window.tools_panel.advert_tab.advert_tab import AdvertTab

import tkinter as tk
import tkinter.ttk as ttk

import typing
if typing.TYPE_CHECKING:
    import src.window.tools_panel as tools_panel_class


class ToolsNotebook(ttk.Notebook):

    master: 'tools_panel_class.ToolsPanel'

    def __init__(self,
                 master: 'tools_panel_class.ToolsPanel'):

        ttk.Notebook.__init__(self, master)

        self.session_tab = SessionTab(self)
        self.settings_tab = SettingsTab(self)
        self.player_tab = PlayerTab(self)
        self.playlist_tab = PlaylistTab(self)
        self.calendar_tab = CalendarTab(self)
        self.exceptions_tab = ExceptionsTab(self)
        self.adverts_tab = AdvertTab(self)

        self.select(4)  # TODO DEBUG

        self.pack(fill=tk.BOTH, expand=True)
