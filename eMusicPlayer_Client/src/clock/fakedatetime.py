
import threading

import datetime as datetime_module


class FakeDatetime(threading.Thread):

    def __init__(self):

        threading.Thread.__init__(self)

        self.speed = 0.01  # ms per thread loop
        self.datetime = datetime_module.datetime.today()

        self.state = False

    def run(self):

        self.state = True

        while self.state:
            self.datetime += datetime_module.timedelta(milliseconds=self.speed)
            #print(self.datetime)
