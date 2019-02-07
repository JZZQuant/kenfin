import datetime
from unittest import TestCase

import schedule
import time

from inference.symbol_factory import TestSymbolFactory
from test_authstack import TestAuthStack


class TestSchedule(TestCase):
    def test_schedule_at(self):
        print(datetime.datetime.now())
        _next = datetime.datetime.now() + datetime.timedelta(seconds=5)

        def job():
            now = datetime.datetime.now()
            print(now)

        schedule.every(2).seconds.do(job)
        schedule.jobs[0].next_run = _next
        while 1:
            schedule.run_pending()
            time.sleep(1)

    def test_schedule_engine(self):
        symbol_factory = TestSymbolFactory(
            [{"symbol": "a"}, {"symbol": "b"}, {"symbol": "c"}, {"symbol": "d"}, {"symbol": "e"}, {"symbol": "f"}, ],TestAuthStack())

        i = 0
        for symbol in symbol_factory.symbols:
            schedule.every(1).minutes.do(symbol.symbol_action)
            # schedule to morning 9:30 , and seperate each symbol by a lapse of a second
            schedule.jobs[-1].next_run = datetime.datetime.now() + datetime.timedelta(seconds=i)
            i += 2

        # look for any new tasks if they are there
        while 1:
            schedule.run_pending()
            # for now 15 seconds is good but ideally this should be decided by the number of lapses in time gap
            time.sleep(1)
