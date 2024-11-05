
from src.funcs import get_flag

import tkinter as tk

import typing

if typing.TYPE_CHECKING:
    import src.window.tools_panel.exceptions_tab.exceptions_tab as exceptions_tab_class


class ExceptionsList(tk.Frame):

    master: 'exceptions_tab_class.ExceptionsTab'

    def __init__(self,
                 master: 'exceptions_tab_class.ExceptionsTab'):

        tk.Frame.__init__(self,
                          master,
                          bd=3,
                          relief=tk.SUNKEN,
                          bg='grey50')

        self.grid(row=1, column=0, sticky=tk.NSEW, padx=2, pady=2)

        self.exceptions = list()
        self.selected_exceptions = set()
        self.clipboard = None
        self.edit_label = None
        self.id_count = 0

    def select(self, arg=None, selected_exception=None):

        if arg is not None:
            ctrl = get_flag(arg.state, 2)
        else:
            ctrl = False

        for exception in self.exceptions:

            if not ctrl:

                if exception.selected:
                    exception.deselect()
                    if exception in self.selected_exceptions:
                        self.selected_exceptions.remove(exception)

                    if exception.editing:
                        exception.set_edit(False)

                elif exception == selected_exception:
                    exception.select()
                    self.selected_exceptions = {selected_exception}

            else:

                if exception == selected_exception:

                    if exception.selected:
                        exception.deselect()
                        self.selected_exceptions.remove(selected_exception)

                    else:
                        exception.select()
                        self.selected_exceptions.add(selected_exception)

                if not len(self.selected_exceptions) == 1:
                    if exception.editing:
                        exception.set_edit(False)

        if self.selected_exceptions:
            self.master.toolbar.set_button_state('delete', True)

            if not any([exception.past or exception.current for exception in self.selected_exceptions]):
                self.master.toolbar.set_button_state('duplicate', True)

            else:
                self.master.toolbar.set_button_state('duplicate', False)

            if (
                    len(self.selected_exceptions) == 1 and
                    not (list(self.selected_exceptions)[0].past or
                         list(self.selected_exceptions)[0].current)
            ):
                self.master.toolbar.set_button_state('edit', True)

            else:
                self.master.toolbar.set_button_state('edit', False)

        else:
            self.master.toolbar.set_button_state('delete', False)
            self.master.toolbar.set_button_state('duplicate', False)

            self.master.toolbar.set_button_state('edit', False)

        self.sort()

    def sort(self):

        self.exceptions.sort()

        for ex in self.exceptions:
            ex.pack_forget()

        for ex in self.exceptions:
            ex.pack(fill=tk.X, expand=True, pady=1)

    def add(self, defaults=(None,)):

        if defaults is None:
            return

        for default in defaults:

            try:
                default_id = default[9]
            except (TypeError, IndexError):
                default_id = None

            exception = ExceptionWidget(master=self,
                                        _id=self.id_count if default_id is None else default_id,
                                        default=default)

            self.exceptions.append(exception)

            self.id_count = (self.id_count if default_id is None else max(default_id, self.id_count)) + 1

        self.sort()

    def delete(self):

        self.main.io_manager.commands('delete_exception', [ex.id for ex in self.selected_exceptions])

        for exception in self.selected_exceptions:
            exception.remove()
            self.exceptions.remove(exception)

        self.selected_exceptions.clear()
        self.select()
        self.sort()

    def edit(self):

        self.edit_label = list(self.selected_exceptions)[0]
        self.edit_label.set_edit(True)

    def duplicate(self):

        self.main.io_manager.commands('duplicate_exception', [ex.id for ex in self.selected_exceptions])

        self.add(list(map(lambda exception: exception.schedule.get_values(), self.selected_exceptions)))

    def remove_past(self):

        past = list(filter(lambda e: e.past, self.exceptions))

        for exception in past:
            exception.disconnect()
            self.exceptions.remove(exception)

    def select_all(self):

        self.selected_exceptions = set(self.exceptions)

    def clear(self):

        self.select_all()
        self.delete()

    def get_exception(self, _id):

        exception = filter_1(lambda ex: ex.id == _id, self.exceptions)

        if exception is None:
            raise ValueError()
        else:
            return exception

    def delete_exceptions(self, _ids):

        self.selected_exceptions = {self.get_exception(_id) for _id in _ids}
        self.delete()

    def duplicate_exceptions(self, _ids):

        self.selected_exceptions = {self.get_exception(_id) for _id in _ids}
        self.duplicate()

    def set(self, exceptions_values):

        self.clear()
        self.add(exceptions_values)

