import datetime

from lib.managers.thread import Thread

from src.clock.fakedatetime import FakeDatetime

import datetime as datetime_module

import typing
if typing.TYPE_CHECKING:
    from src import main_manager as main_manager_class
    from src.schedule import exception as exception_class


class ClockManager(Thread):

    __doc__ = """
    Manage realtime clock.
    Interface between scheduling datas <-> Player actions
    """

    fake_datetime = True

    main_manager: 'main_manager_class.MainManager'

    def __init__(self,
                 main_manager: 'main_manager_class.MainManager'):

        Thread.__init__(self, main_manager=main_manager)

        self.pause_state = True
        self.state = False

        self.last_test = None

        self.current_exception: typing.Optional['exception_class.ScheduleException'] = None

        self.fake_datetime_instance: typing.Optional['FakeDatetime'] = None

    def set_pause_state(self, state: bool):

        self.pause_state = state

        self.log(f"Clock manager pause state set to {self.pause_state}")

        self.test_current_state()

    def load(self):

        if self.fake_datetime:

            self.fake_datetime_instance = FakeDatetime()
            self.fake_datetime_instance.start()

    def get_now(self):
        if self.fake_datetime:
            return self.fake_datetime_instance.datetime
        else:
            return datetime_module.datetime.today()

    @staticmethod
    def get_weekday(year: int, month: int, day: int):
        return datetime_module.datetime(year, month, day).weekday()

    def update(self):

        Thread.update(self)

        if self.test_time():
            self.test_current_state()

    def test_time(self):
        """Return True if a quarter hour passed"""

        now = self.get_now()

        if self.last_test is None:

            self.last_test = datetime.datetime(year=now.year,
                                               month=now.month,
                                               day=now.day,
                                               hour=now.hour,
                                               minute=(now.minute//15)*15,
                                               second=now.second)
            return True

        next_test = self.last_test + datetime.timedelta(minutes=15)

        if now >= next_test:

            self.last_test = next_test
            return True

        return False

    def test_current_state(self):
        """Test if play state is coherent with scheduling"""

        self.test_exception()

        if self.current_exception is None:

            schedule_state = self.main_manager.schedule_manager.calendar.get_at(self.get_now())
            self.set_state(schedule_state)

    def test_exception(self):
        """Test if any exception is reached or if current is passed"""

        if self.current_exception is None:

            next_exception = self.main_manager.schedule_manager.get_current_exception()

            if next_exception is not None:
                self.log(f"Found exception: {next_exception.prompt()}")
                self.set_state(next_exception.action)
                self.current_exception = next_exception

        else:
            if self.current_exception.is_passed():
                self.current_exception = None

    def set_state(self, state):
        """Set the state of the clock_manager and player_manager"""

        if state != self.state:

            if not self.pause_state:

                if state and not self.state:
                    self.main_manager.player_manager.execute('begin')
                    self.log("Schedule state set to True")

                elif not state and self.state:
                    self.main_manager.player_manager.execute('end')
                    self.log("Schedule state set to False")

                self.state = state

    def quit(self):

        self.log("Quitting...")

        if self.fake_datetime:
            self.fake_datetime_instance.state = False
            self.fake_datetime_instance.join()
