
from src.window.tools_panel.tab_widget import TabWidget
from src.window.tools_panel.player_tab.playlist_frame import PlaylistFrame
from src.window.tools_panel.player_tab.control_frame import ControlBar
from src.window.tools_panel.player_tab.progress_frame import ProgressBar

import tkinter as tk

import typing
if typing.TYPE_CHECKING:
    import src.window.tools_panel.tools_notebook as tools_notebook_class


class PlayerTab(TabWidget):

    master: 'tools_notebook_class.ToolsNotebook'

    def __init__(self,
                 master: 'tools_notebook_class.ToolsNotebook'):

        TabWidget.__init__(self,
                           master,
                           name='Player',
                           icon='player')

        self.playlist_frame = PlaylistFrame(self)
        self.control_frame = ControlBar(self)
        self.progress_bar_frame = ProgressBar(self)
