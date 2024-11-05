
import typing
if typing.TYPE_CHECKING:
    import src.window.tools_panel.calendar_tab.day_canvas as day_canvas_class


class CalendarSlot:

    def __repr__(self):
        return f"<ScheduleCalendarSlot {str(self.hour).zfill(2)}:{str(self.quarter * 15).zfill(2)})>"

    def __init__(self,
                 canvas: 'day_canvas_class.DayCanvas',
                 hour: int,
                 quarter: int):

        self.canvas = canvas

        self.hour = hour
        self.quarter = quarter

        self.w = self.canvas.w
        self.h = int((self.canvas.h - 2 * self.canvas.width) / (24 * 4))
        self.x = 0
        self.y = (4 * self.hour + self.quarter) * self.h + self.canvas.width

        self.index = self.canvas.create_rectangle(self.x, self.y,
                                                  self.x + self.w, self.y + self.h,
                                                  outline='')

        self.exception = None
        self.state = False
        self.hovered = False
        self.state_lock = False

        self.update()

    def set_state(self,
                  state: bool):

        self.state = state

        self.update()

    def update(self):

        if self.exception is None:

            if self.state:
                color = '#6464C8'

            else:
                color = '#9696FA'

        else:

            if self.exception.datetime.action == 0:

                if self.state:
                    color = '#C86464'

                else:
                    color = '#FA9696'

            elif self.exception.datetime.action == 1:

                if self.state:
                    color = '#64C864'

                else:
                    color = '#96FA96'

            else:
                color = '#000000'

        self.canvas.itemconfigure(self.index, fill=color)

    def get_time(self):
        return self.hour, self.quarter

    def update_exception(self,
                         exception,
                         remove):

        datetime = exception.datetime
        # weekday = self.canvas.main.schedule_manager.get_weekday(datetime.year, datetime.month, datetime.day) TODO
        weekday = 0

        is_in_exception = (

                weekday == self.canvas.master.day and

                (
                        (self.hour == datetime.start_hour != datetime.end_hour
                         and
                         self.quarter * 15 >= datetime.start_minute)
                        or
                        datetime.start_hour < self.hour < datetime.end_hour
                        or
                        (self.hour == datetime.end_hour
                         and
                         self.quarter * 15 < datetime.end_minute)
                )
        )

        if self.exception is exception and (not is_in_exception or remove):
            self.exception = None

        if self.exception is not exception and is_in_exception and not remove:
            self.exception = exception

        self.update()
