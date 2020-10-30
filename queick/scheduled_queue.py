import sched, time
import traceback
import pdb

class ScheduledQueue:
    def __init__(self):
        self.queue = sched.scheduler(time.time, time.sleep)

    def enqueue(self, job):
        try:
            self.queue.enterabs(job.start_at, job.priority, job.func, argument=(job.args,))
            self.queue.run()
        except Exception as e:
            traceback.print_exc()
