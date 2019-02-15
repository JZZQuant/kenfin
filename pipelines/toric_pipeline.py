import time
from datetime import datetime, timedelta

import schedule

from connector.auth_stack import AuthSingletonStack
from logger.heirarchical_logger import info


class ToricPipeline(object):
    def __init__(self, start_time, end_time, jobs, intra_action_delta=15, execution_heart_beat=1,
                 schedule_heart_beat=60):
        self.start_time = start_time
        self.end_time = end_time
        self.jobs = jobs
        self.intra_action_delta = intra_action_delta
        self.execution_heart_beat = execution_heart_beat
        self.schedule_heart_beat = schedule_heart_beat

    def trigger(self):
        i = 0
        now = datetime.now()
        tomorrow = (datetime.today() + timedelta(days=1)).replace(hour=1)
        start = now.replace(hour=self.start_time[0], minute=self.start_time[1], second=self.start_time[2])
        close = now.replace(hour=self.end_time[0], minute=self.end_time[1], second=self.end_time[2])
        next_run = max(start, now)

        for job in self.jobs:
            schedule.every(self.schedule_heart_beat).seconds.do(job)
            schedule.jobs[-1].next_run = next_run.replace(second=i)
            i += self.intra_action_delta

        # look for any new tasks if they are there
        while datetime.now() < close:
            schedule.run_pending()
            time.sleep(self.execution_heart_beat)

        schedule.clear()
        AuthSingletonStack.__reset__()
        while close < datetime.now() < tomorrow:
            info("Done with daily execution: breaking out of the inner circle")
            # uncomment this and comment the break in case this program where to run forever,
            # time.sleep(30)
            break
