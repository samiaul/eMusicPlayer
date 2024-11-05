
from src.window.tools_panel.tab_widget import TabWidget
from src.window.tools_panel.calendar_tab.calendar_tool_bar import CalendarToolBar
from src.window.tools_panel.calendar_tab.day_frame import DayFrame
from src.funcs import get_flag, each

import tkinter as tk

import typing
if typing.TYPE_CHECKING:
    import src.window.tools_panel.tools_notebook as tools_notebook_class
    import src.window.tools_panel.calendar_tab.day_canvas as day_canvas_class

    SCHEDULE_TYPE = typing.Dict[typing.Tuple[int, int], bool]


class CalendarTab(TabWidget):

    master: 'tools_notebook_class.ToolsNotebook'

    ALL_DAY = {(i // 4, i % 4): True for i in range(96)}
    ALL_NIGHT = {(i // 4, i % 4): False for i in range(96)}

    def __init__(self,
                 master: 'tools_notebook_class.ToolsNotebook'):

        TabWidget.__init__(self,
                           master,
                           name='Calendar',
                           icon='calendar',
                           bd=3,
                           relief=tk.SUNKEN)

        self.scrollbar = tk.Scrollbar(self,
                                      orient=tk.VERTICAL,
                                      command=self.scroll_bar)
        self.scrollbar.grid(row=0, column=0, sticky=tk.NS)

        self.toolbar = CalendarToolBar(self)

        self.day_frames: typing.Tuple[DayFrame, ...] = tuple([DayFrame(master=self, day=day) for day in range(7)])
        self.clipboard = None
        self.selected_days: typing.Set[int] = set()

        self.select(day=0)

        self.grid_rowconfigure(0, weight=1)

    def get_canvas(self) -> typing.Tuple['day_canvas_class.DayCanvas', ...]:

        return tuple(map(lambda day_frame: day_frame.canvas, self.day_frames))

    def scroll_wheel(self,
                     event: tk.Event):

        for canvas in self.get_canvas():
            canvas.yview_scroll(-1 * (event.delta // 120), 'units')

    def scroll_bar(self, *args):

        for canvas in self.get_canvas():
            canvas.yview(*args)

    def select(self,
               event=None,
               day=-1):

        if event is not None:
            ctrl = get_flag(event.state, 2)
        else:
            ctrl = False

        for day_frame in self.day_frames:

            if not ctrl:

                if day_frame.selected:
                    day_frame.deselect()

                elif day_frame.day == day:
                    day_frame.select()
                    self.selected_days = {day}

            elif day_frame.day == day:

                if day_frame.selected:
                    day_frame.deselect()
                    self.selected_days.remove(day)
                else:
                    day_frame.select()
                    self.selected_days.add(day)

        if not len(self.selected_days) == 1:
            self.toolbar.set_button_state('copy', False)
        else:
            self.toolbar.set_button_state('copy', True)

    def update_other_days(self,
                          day: int,
                          schedule: 'SCHEDULE_TYPE'):

        for day_frame in self.day_frames:

            if not day_frame.day == day and day_frame.selected:
                day_frame.canvas.set_schedule(schedule)

    def paste_to(self,
                 day: int):
        self.day_frames[day].canvas.set_schedule(self.clipboard)

    def day_to(self,
               day: int):
        self.day_frames[day].canvas.set_schedule(self.ALL_DAY)

    def night_to(self,
                 day: int):
        self.day_frames[day].canvas.set_schedule(self.ALL_NIGHT)

    def invert_to(self,
                  day: int):
        inverted = {time: not state for time, state in self.day_frames[day].canvas.get_schedule().items()}
        self.day_frames[day].canvas.set_schedule(inverted)

    def copy(self):
        self.clipboard = self.day_frames[tuple(self.selected_days)[0]].canvas.get_schedule()
        self.toolbar.set_button_state('paste', True)

    def paste(self):

        each(self.paste_to, self.selected_days)

    def day(self):

        each(self.day_to, self.selected_days)

    def night(self):

        each(self.night_to, self.selected_days)

    def invert(self):

        each(self.invert_to, self.selected_days)

    def clear(self):

        each(self.night_to, range(7))

    def update_exception(self,
                         exception,
                         remove=False):

        datetime = exception.datetime

        """
        if self.main.schedule_manager.is_this_week(datetime.year, datetime.month, datetime.day):
            for canvas in self.get_canvas():
                for slot in canvas.slots:
                    slot.update_exception(exception, remove)
        """

    def update_advert(self,
                      advert,
                      remove=False):

        for day_frame in self.day_frames:
            day_frame.canvas.update_advert(advert, remove)

    def get_calendar(self):

        calendar = list()

        for canvas in self.get_canvas():

            day_list = list()

            curr_state = False
            slot = None
            part = list()

            for slot in canvas.slots:

                if slot.state != curr_state:
                    part.append((slot.hour, slot.quarter))

                    if slot.state and not curr_state:
                        curr_state = True

                    elif not slot.state and curr_state:
                        curr_state = False

                        day_list.append(part)

                        part = list()

            if curr_state:
                part.append((slot.hour, slot.quarter+1))
                day_list.append(part)

            calendar.append(day_list)

        return calendar

    def set_calendar(self,
                     calendar):

        self.clear()

        if calendar is None:
            return

        day_canvas_list = self.get_canvas()

        for day_index in range(7):

            day_datas = calendar[day_index]
            day_canvas = day_canvas_list[day_index]

            for part in day_datas:

                start_hour, start_quarter = part[0]
                end_hour, end_quarter = part[1]

                for j in range(start_hour * 4 + start_quarter, end_hour * 4 + end_quarter):
                    day_canvas.get_slot_by_time(j // 4, j % 4).set_state(True)
