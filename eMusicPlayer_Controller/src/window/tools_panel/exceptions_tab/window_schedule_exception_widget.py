
from assets.window_schedule_exception_datetime import ExceptionDatetime
from assets.funcs import get_root, get_char_width, get_state, var_holder

import tkinter as tk


class ExceptionWidget(tk.Frame):

    def __lt__(self, other):

        return self.datetime < other.datetime

    def __init__(self, master, _id, default=None):

        tk.Frame.__init__(self, master=master)

        self.main = master.main

        self['bd'] = 2
        self['relief'] = tk.RIDGE

        self.id = _id

        self.widgets = list()
        self.spinboxes = list()

        self.datetime = ExceptionDatetime(parent=self, default=default)

        self.selected = False
        self.editing = False
        self.past = False
        self.current = False

        self.add_label(text=self.main.lang_manager.schedule.exceptions.label[0])

        self.add_spinbox(variable=self.datetime.year_var,
                         format_="%04.0f",
                         width=5)

        self.add_label(text="/")

        self.add_spinbox(variable=self.datetime.month_var,
                         format_="%02.0f",
                         width=10)

        self.add_label(text="/")

        self.add_spinbox(variable=self.datetime.day_var,
                         format_="%02.0f")

        self.add_label(text=self.main.lang_manager.schedule.exceptions.label[1])

        self.add_spinbox(variable=self.datetime.start_hour_var,
                         format_="%02.0f")

        self.add_label(text="h")

        self.add_spinbox(step=15,
                         variable=self.datetime.start_minute_var,
                         format_="%02.0f")

        self.add_label(text=self.main.lang_manager.schedule.exceptions.label[2])

        self.add_spinbox(variable=self.datetime.end_hour_var,
                         format_="%02.0f")

        self.add_label(text="h")

        self.add_spinbox(step=15,
                         variable=self.datetime.end_minute_var,
                         format_="%02.0f")

        self.add_label(text=" : ")

        self.add_spinbox(variable=self.datetime.action_var,
                         values=self.main.schedule_manager.ACTIONS,
                         width=get_char_width(self.main.schedule_manager.ACTIONS))

        self.add_label(text=self.main.lang_manager.schedule.exceptions.label[3])

        self.add_entry(variable=self.datetime.object)

        self.bind('<Button-1>', lambda arg: self.master.select(arg, self))

        self.set_edit(False)

        self.update_spinboxes()

        self.pack(fill=tk.X, expand=True, pady=1)

    def add_label(self,
                  text):

        label = tk.Label(master=self,
                         text=str(text))

        label.bind('<Button-1>', lambda arg: self.master.select(arg, self))

        self.widgets.append(label)

    def add_spinbox(self,
                    variable,
                    step=None,
                    format_=None,
                    values=None,
                    state=True,
                    width=3):

        with var_holder(variable):

            spinbox = tk.Spinbox(master=self,
                                 increment=step,
                                 command=self.update_spinboxes,
                                 textvariable=variable,
                                 values=values,
                                 format=format_,
                                 width=width,
                                 wrap=True,
                                 state=get_state(state, readonly=True))

        self.widgets.append(spinbox)
        self.spinboxes.append(spinbox)

        self.add_varlabel(variable=variable)

    def add_entry(self,
                  variable,
                  width=15):

        spinbox = tk.Entry(master=self,
                           textvariable=variable,
                           width=width)

        self.widgets.append(spinbox)

        self.add_varlabel(variable=variable)

    def add_varlabel(self,
                     variable):

        varlabel = VarLabel(master=self,
                            textvariable=variable)

        varlabel.bind('<Button-1>', lambda arg: self.master.select(arg, self))

        self.widgets.append(varlabel)

    def select(self):

        self.selected = True

        self.update_color()

    def deselect(self):

        self.selected = False

        self.update_color()

    def set_edit(self, state):

        if self.editing != state and not state:
            self.main.io_manager.commands('update_exception', self.id)

        self.editing = state

        for widget in self.widgets:
            widget.pack_forget()

        for widget in self.widgets:

            if widget.__class__ == tk.Label:
                widget.pack(side=tk.LEFT)

            elif widget.__class__ in (tk.Spinbox, tk.Entry):
                if state:
                    widget.pack(side=tk.LEFT)

            elif widget.__class__ == VarLabel:
                if not state:
                    widget.pack(side=tk.LEFT)

        self.update_spinboxes()

    def set_past(self):

        self.past = True

        self.set_edit(False)

        self.update_color()

    def set_current(self):

        self.current = True

        self.set_edit(False)

        self.update_color()

    def update_spinboxes(self):

        self.datetime.update_values()

        possibilities = self.datetime.get_ranges()

        self.spinboxes[0]['to'], self.spinboxes[0]['from_'] = possibilities[0][::-1]
        # self.spinboxes[1]['values'] = possibilities[1] TODO
        self.spinboxes[1]['to'], self.spinboxes[1]['from_'] = possibilities[1][::-1]  # TODO
        self.spinboxes[2]['to'], self.spinboxes[2]['from_'] = possibilities[2][::-1]
        self.spinboxes[3]['to'], self.spinboxes[3]['from_'] = possibilities[3][::-1]
        self.spinboxes[4]['to'], self.spinboxes[4]['from_'] = possibilities[4][::-1]
        self.spinboxes[5]['to'], self.spinboxes[5]['from_'] = possibilities[5][::-1]
        self.spinboxes[6]['to'], self.spinboxes[6]['from_'] = possibilities[6][::-1]

        get_root(self).schedule_panel.get_frame(0).update_exception(self)

    def remove(self):

        self.destroy()

        get_root(self).schedule_panel.get_frame(0).update_exception(self, remove=True)

    def update_color(self):

        if self.selected:

            if self.past:
                color = '#C86464'

            elif self.current:
                color = '#64C864'

            else:
                color = '#96C8E1'

        else:

            if self.past:
                color = '#FA9696'

            elif self.current:
                color = '#96FA96'

            else:
                color = self.master.master.cget('bg')

        self['bg'] = color

        for widget in filter(lambda w: w.__class__ in (tk.Label, VarLabel), self.widgets):
            widget['bg'] = color


class VarLabel(tk.Label):

    def __init__(self, master, textvariable):
        tk.Label.__init__(self, master=master, textvariable=textvariable)
