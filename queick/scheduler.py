import sched
import time
from logging import getLogger

logger = getLogger(__name__)

class Scheduler:
    def __init__(self):
        self.queue = sched.scheduler(time.time, time.sleep)

    def put(self, job):
        self.queue.enterabs(job.start_at, job.priority, job.func, argument=(job.args,))

    def run(self):
        self.queue.run()
