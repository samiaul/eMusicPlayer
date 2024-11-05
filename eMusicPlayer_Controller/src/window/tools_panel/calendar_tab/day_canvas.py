
from src.window.tools_panel.calendar_tab.calendar_slot import CalendarSlot
from src.funcs import get_flag, each

import tkinter as tk

import typing
if typing.TYPE_CHECKING:
    import src.window.tools_panel.calendar_tab.day_frame as day_frame_class
    from calendar_tab import SCHEDULE_TYPE


class DayCanvas(tk.Canvas):

    master: 'day_frame_class.DayFrame'

    HEIGHT_FACTOR = 10
    WIDTH = 80

    def __init__(self, master: 'day_frame_class.DayFrame'):

        self.width = 1.5
        self.w = self.WIDTH
        self.h = self.HEIGHT_FACTOR * 24 * 4 + 2 * self.width

        tk.Canvas.__init__(self,
                           master=master,
                           bd=-2,
                           width=self.w,
                           height=300,
                           scrollregion=(0, 0, self.w, self.h))

        self.pack(fill=tk.BOTH, expand=True)

        self.config(yscrollcommand=self.master.master.scrollbar.set)

        self.slots: typing.List[CalendarSlot] = list()
        self.button_state = False
        self.adverts = dict()  # TODO TYPING
        self.shift = False

        self.hour_height = (self.h - 2 * self.width) // 24
        self.half_height = self.hour_height / 2
        self.quarter_height = self.half_height / 2
        self.twelfth_height = self.quarter_height / 3
        self.half_width = self.w // 2
        self.quarter_width = self.half_width / 2

        self.half_dash = self.half_height
        self.quarter_dash = 1

        self.cursor_x = 0
        self.cursor_y = 0

        for hour in range(24):

            for quarter in range(4):

                self.slots.append(CalendarSlot(self, hour, quarter))

                if quarter in (1, 3):
                    self.draw_quarter_line(hour, quarter)

            self.draw_text(hour)
            self.draw_hour_line(hour)
            self.draw_half_line(hour)

        self.marker = self.create_line(0,
                                       0,
                                       self.w,
                                       0,
                                       fill='red',
                                       width='2')

        self.create_rectangle(self.width // 2,
                              self.width // 2,
                              self.w - self.width // 2,
                              self.h - self.width // 2,
                              outline='black',
                              width=self.width)

        self.bind('<ButtonPress-1>', self.left_button_press)
        self.bind('<ButtonRelease-1>', self.left_button_release)
        self.bind('<Motion>', self.hover_slot)

    def draw_text(self,
                  hour: int):

        x = self.w - self.width - 6
        y = hour * (self.h - 2 * self.width) // 24 + self.width + 6

        self.create_text(x,
                         y,
                         anchor=tk.CENTER,
                         text=f"{str(hour).zfill(2)}h",
                         font='Arial 6 bold')

    def draw_hour_line(self,
                       hour: int):

        y = hour * self.hour_height + self.width

        self.create_line(0,
                         y,
                         self.w,
                         y,
                         width='1')

    def draw_half_line(self,
                       hour: int):

        y = (hour + 0.5) * self.hour_height + self.width

        self.create_line(0,
                         y,
                         self.w // 2,
                         y,
                         width='1')

    def draw_quarter_line(self,
                          hour: int,
                          quarter: int):

        y = (4 * hour + quarter) * self.quarter_height + self.width

        self.create_line(0,
                         y,
                         self.w // 4,
                         y,
                         width='1')

    def left_button_press(self, event: tk.Event):

        self.button_state = True

        if not self.master.selected:
            self.master.master.select(event, self.master.day)

        if not get_flag(event.state, 0):
            self.switch_state(self.get_hovered_slots())
            self.shift = False

        else:
            self.shift = True
            self.goto_exception(self.get_hovered_slot())
            self.goto_advert(event.x, event.y)

    def left_button_release(self,
                            event: tk.Event):

        self.button_state = False

        for slot in self.slots:
            slot.state_lock = False

        # TODO UPDATE SCHEDULE

        self.shift = False

    def goto_exception(self, hovered_slot):
        if hovered_slot.exception is not None:
            pass
            # self.main.window.schedule_panel.goto_exception(hovered_slot.exception) TODO

    def goto_advert(self,
                    cursor_x: int,
                    cursor_y: int):

        for advert, marker in self.adverts.items():
            if marker == self.find_closest(cursor_x, cursor_y)[0]:
                # self.main.window.schedule_panel.goto_advert(advert) TODO
                return

    def update_marker(self,
                      hour: int,
                      minute: int):

        if hour == 23 and minute == 59:
            y = 0
        else:
            y = hour * self.hour_height + (minute / 15) * self.quarter_height + self.width

        self.coords(self.marker, 0, y, self.w, y)

    def hover_slot(self, event: tk.Event):

        self.cursor_x = event.x
        self.cursor_y = event.y

        hovered_slots = self.get_hovered_slots()

        if hovered_slots is not None:

            if self.button_state:
                self.switch_state(hovered_slots)

            unhovered_slots = filter(lambda s: s not in hovered_slots, self.slots)

            for slot in unhovered_slots:
                slot.hovered = False
                slot.state_lock = False

    def get_hovered_slot(self):

        y = self.cursor_y + self.get_y_scroll() - self.width
        hour = int(y / self.hour_height)
        quarter = int(y / self.quarter_height) - 4 * hour
        return self.get_slot_by_time(hour, quarter)

        # return self.get_slot_by_index(self.find_closest(self.cursor_x, self.cursor_y + self.get_y_scroll())[0])

    def get_hovered_slots(self):

        y = self.cursor_y + self.get_y_scroll() - self.width

        if 0 < self.cursor_x < self.quarter_width:
            return (
                self.get_hovered_slot(),
            )

            # hour = y // self.hour_height
            # quarter = y // self.quarter_height - 4 * hour
            # return (
            #     self.get_slot_by_time(hour, quarter),
            # )

        elif self.quarter_width < self.cursor_x < self.half_width:
            hour = int(y / self.hour_height)
            half = int(y / self.half_height - 2 * hour) * 2
            return (
                self.get_slot_by_time(hour, half),
                self.get_slot_by_time(hour, half + 1)
            )

        elif self.half_width < self.cursor_x < self.w:
            hour = int(y / self.hour_height)
            return (
                self.get_slot_by_time(hour, 0),
                self.get_slot_by_time(hour, 1),
                self.get_slot_by_time(hour, 2),
                self.get_slot_by_time(hour, 3)
            )

    def get_y_scroll(self):

        return max(int(self.master.master.scrollbar.get()[1] * self.h - self.winfo_height()), 0)

    def get_slot_by_index(self,
                          index: int):

        try:
            return tuple(filter(lambda slot: slot.index == index, self.slots))[0]
        except IndexError:
            return None

    def get_slot_by_time(self,
                         hour: int,
                         quarter: int):

        try:
            return tuple(filter(lambda slot: slot.hour == hour and slot.quarter == quarter, self.slots))[0]
        except IndexError:
            return None

    def switch_state(self,
                     hovered_slots: typing.Tuple[CalendarSlot]):

        hovered_slot = self.get_hovered_slot()

        if hovered_slot is not None and hovered_slots is not None:

            last_edit = dict()

            if not hovered_slot.state_lock:
                hovered_slot.set_state(not hovered_slot.state)
                last_edit[hovered_slot.get_time()] = hovered_slot.state
                hovered_slot.state_lock = True

            for slot in hovered_slots:
                if slot is not hovered_slot:
                    if not slot.state_lock:
                        slot.set_state(hovered_slot.state)
                        last_edit[slot.get_time()] = slot.state
                        slot.state_lock = True

            self.master.master.update_other_days(self.master.day, last_edit)

    def get_schedule(self) -> 'SCHEDULE_TYPE':

        return {(slot.hour, slot.quarter): slot.state for slot in self.slots}

    def set_schedule(self,
                     schedule: 'SCHEDULE_TYPE'):

        each(lambda x: self.get_slot_by_time(*x[0]).set_state(x[1]), schedule.items())

    def get_current_state(self,
                          hour: int,
                          minute: int):

        return self.get_slot_by_time(hour, minute // 15).state

    def update_advert(self, advert, remove):

        if self.master.day not in advert.schedule.get_days():
            remove = True

        if remove:

            try:
                advert_marker = self.adverts[advert]

            except KeyError:
                pass

            else:
                self.delete(advert_marker)

        else:

            hour, minute = advert.schedule.get_values()[2:4]
            twelfth = minute / 5
            y = (12 * hour + twelfth) * self.twelfth_height + self.width

            try:
                advert_marker = self.adverts[advert]

            except KeyError:

                advert_marker = self.create_line(0,
                                                 y,
                                                 self.w,
                                                 y,
                                                 fill='yellow',
                                                 width='2')

                self.adverts[advert] = advert_marker

            else:
                self.coords(advert_marker, 0, y, self.w, y)
