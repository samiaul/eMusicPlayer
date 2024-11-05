
from src.window.tools_panel.tab_widget import TabWidget
from src.window.tools_panel.exceptions_tab.exceptions_tool_bar import ExceptionsToolBar
from src.window.tools_panel.exceptions_tab.exceptions_list import ExceptionsList

import tkinter as tk

import typing
if typing.TYPE_CHECKING:
    import src.window.tools_panel.tools_notebook as tools_notebook_class


class ExceptionsTab(TabWidget):

    master: 'tools_notebook_class.ToolsNotebook'

    def __init__(self,
                 master: 'tools_notebook_class.ToolsNotebook'):

        TabWidget.__init__(self,
                           master,
                           name='Exceptions',
                           icon='exception')

        self.toolbar = ExceptionsToolBar(self)
        self.exceptions_list = ExceptionsList(self)
