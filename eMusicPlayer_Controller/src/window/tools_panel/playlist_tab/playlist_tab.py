
from src.window.tools_panel.tab_widget import TabWidget

import tkinter as tk

import typing
if typing.TYPE_CHECKING:
    import src.window.tools_panel.tools_notebook as tools_notebook_class


class PlaylistTab(TabWidget):

    master: 'tools_notebook_class.ToolsNotebook'

    def __init__(self,
                 master: 'tools_notebook_class.ToolsNotebook'):

        TabWidget.__init__(self,
                           master,
                           name='Playlist',
                           icon='playlist')
