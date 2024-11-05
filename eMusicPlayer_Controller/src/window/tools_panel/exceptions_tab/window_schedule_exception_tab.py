
from assets.funcs import filter_1, get_flag
from assets.window_widget_notebook import NotebookTabType
from assets.window_schedule_exception_toolbar import ExceptionsToolBar
from assets.window_schedule_exception_widget import ExceptionWidget

import tkinter as tk


class ExceptionsTab(NotebookTabType):

    def __init__(self, master, index):
        self.main = master.main

        NotebookTabType.__init__(self,
                                 master=master,
                                 index=index,
                                 name=self.main.lang_manager.schedule.exceptions.title,
                                 frame=ExceptionFrame,
                                 image='exception')

        self.toolbar = ExceptionsToolBar(master=self)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.grid_columnconfigure(0, weight=1)

    def deselect_tab(self):
        NotebookTabType.deselect_tab(self)

        self.frame.select()


class ExceptionFrame(tk.Frame):

    def __init__(self, master):

        tk.Frame.__init__(self, master=master)

        self.main = master.main