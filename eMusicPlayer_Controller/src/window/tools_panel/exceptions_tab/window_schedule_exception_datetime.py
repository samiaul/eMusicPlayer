
import tkinter as tk


class ExceptionDatetime:

    def __init__(self, parent, default):

        self.parent = parent

        self.main = self.parent.main

        self.year = None
        self.month = None
        self.day = None
        self.start_hour = None
        self.start_minute = None
        self.end_hour = None
        self.end_minute = None
        self.action = None
        self.object = None

        self.year_var = tk.StringVar(parent)
        self.month_var = tk.StringVar(parent)
        self.day_var = tk.StringVar(parent)
        self.start_hour_var = tk.StringVar(parent)
        self.start_minute_var = tk.StringVar(parent)
        self.end_hour_var = tk.StringVar(parent)
        self.end_minute_var = tk.StringVar(parent)
        self.action_var = tk.StringVar(parent)
        self.object_var = tk.StringVar(parent)

        self.set_values(self.get_default() if default is None else default)

    def __cmp__(self, other):

        self_start = self.get_values()[0:5]
        other_start = other.get_values()[0:5]

        for s, o in zip(self_start, other_start):
            if s < o:
                return -1
            elif s > o:
                return 1
            elif s == o:
                continue
        return 0

    def __lt__(self, other):

        return self.__cmp__(other) == -1

    def verify(self):

        default = self.get_default()

        if self.year <= default[0]:
            self.year = default[0]

            if self.month <= default[1]:
                self.month = default[1]

                if self.day <= default[2]:
                    self.day = default[2]

                    if self.start_hour <= default[3]:
                        self.start_hour = default[3]

                        if self.start_minute <= default[4]:
                            self.start_minute = default[4]

        if self.end_hour <= self.start_hour:
            self.end_hour = self.start_hour

            if self.end_minute <= self.end_minute:
                self.end_minute = self.end_minute

        self.update_vars()

    def get_values(self):

        return (
            self.year,
            self.month,
            self.day,
            self.start_hour,
            self.start_minute,
            self.end_hour,
            self.end_minute,
            self.action,
            self.object
        )

    def set_values(self, values):

        self.year = values[0]
        self.month = values[1]
        self.day = values[2]
        self.start_hour = values[3]
        self.start_minute = values[4]
        self.end_hour = values[5]
        self.end_minute = values[6]
        self.action = values[7]
        self.object = values[8]

        self.update_vars()

    def update_vars(self):

        self.year_var.set(str(self.year).zfill(4))
        # self.month_var.set(self.main.schedule_manager.months[self.month]) TODO
        self.month_var.set(str(self.month).zfill(2))  # TODO
        self.day_var.set(str(self.day).zfill(2))
        self.start_hour_var.set(str(self.start_hour).zfill(2))
        self.start_minute_var.set(str(self.start_minute).zfill(2))
        self.end_hour_var.set(str(self.end_hour).zfill(2))
        self.end_minute_var.set(str(self.end_minute).zfill(2))
        self.action_var.set(self.main.schedule_manager.ACTIONS[self.action])
        self.object_var.set(self.object)

    def update_values(self):

        self.year = int(self.year_var.get())
        # self.month = self.main.schedule_manager.months.index(self.month_var.get()) TODO
        self.month = int(self.month_var.get())
        self.day = int(self.day_var.get())
        self.start_hour = int(self.start_hour_var.get())
        self.start_minute = int(self.start_minute_var.get())
        self.end_hour = int(self.end_hour_var.get())
        self.end_minute = int(self.end_minute_var.get())
        self.action = self.main.schedule_manager.ACTIONS.index(self.action_var.get())
        self.object = self.object_var.get()

        self.verify()

    def get_ranges(self):

        default = self.get_default()
        values = self.get_values()

        return (
            (default[0],
             default[0] + 1),

            # self.main.schedule_manager.months[(default[1]-1 if self.year == default[0] else 0):], TODO
            (default[1] if values[0] == default[0] else 1,
             12),

            (default[2] if values[0:2] == default[0:2] else 1,
             self.main.schedule_manager.get_month_length(self.year, self.month)),

            (default[3] if values[0:3] == default[0:3] else 0,
             23),

            (default[4] if values[0:4] == default[0:4] else 0,
             45),

            (self.start_hour + int(self.start_minute >= 45),
             23),

            ((((self.start_minute + 15) % 60) if values[5] == values[3] else 0),
             45)
        )

    def get_default(self):

        now = self.main.schedule_manager.get_now()

        return (
            *now[0:3],
            (now[4] + int(now[5] >= 45)),  # Next hour if minutes >= 45
            ((now[5] // 15 + 1) * 15) % 60,  # Round minute to next multiple of 15|mod(60)
            (now[4] + int((now[5] + 15) >= 45)),  # Next hour if minutes >= 45
            ((now[5] // 15 + 2) * 15) % 60,  # Round minute to second next multiple of 15|mod(60)
            0,
            ""
        )

    def get_date(self):
        return self.year, self.month, self.day

    def get_start_time(self):
        return self.start_hour, self.start_minute

    def get_end_time(self):
        return self.end_hour, self.end_minute
