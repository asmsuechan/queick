import socket
import pickle
from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor
from logging import getLogger
import os

from .job import Job

logger = getLogger(__name__)


class QueueManager:
    def __init__(self, queue_class=None):
        qc = queue_class or Queue
        self.queue = qc()

    def enqueue(self, value):
        logger.debug('[QueueManager] Job is queued: %s', value)
        self.queue.put(value)

    def dequeue(self):
        return self.queue.get()

    def is_empty(self):
        return self.queue.empty()

    def create_job(self, *args, **kwargs):
        return Job(*args, **kwargs)

    def watch(self, event, scheduler, nw):
        event.wait()
        while True:
            while self.is_empty() != True:
                data = self.dequeue()
                logger.debug('[QueueManager] Job is dequeued: %s', data)

                max_workers = os.cpu_count()
                executor = ThreadPoolExecutor(max_workers=max_workers)
                job = self.create_job(
                    data['func_name'],
                    data['args'],
                    executor,
                    scheduler,
                    nw,
                    retry=data['retry'],
                    retry_interval=data['retry_interval'],
                    retry_type=data['retry_type'],
                    retry_on_network_available=data['retry_on_network_available'])
                # Scheduled job by q.schedule_at()
                if 'start_at' in data:
                    job.start_at = data['start_at']
                    # Cron job by q.cron()
                    if 'interval' in data:
                        job.cron_interval = data['interval']
                        job.cron = True
                    scheduler.put(job)
                    scheduler.run()
                else:
                    job.perform()

            event.clear()
            if self.is_empty():
                event.wait()
