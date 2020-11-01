from multiprocessing import Process, Queue, Event
import socket
import pickle
import time
import importlib

from .queue_manager import QueueManager
from .job_receiver import JobReceiver
from .scheduler import Scheduler
from .logger import logger

class Worker:
    def work(self):
        try:
            event = Event()
            qm = QueueManager(queue_class=Queue)
            scheduler = Scheduler()

            jr = JobReceiver()
            p = Process(target=jr.listen, args=(event, qm,))
            p.start()

            qm.watch(event, scheduler)

        except KeyboardInterrupt:
            p.terminate()
            for job in scheduler.queue.queue:
                scheduler.queue.cancel(job)
            logger.info("Stopping... Press Ctrl+C to exit immediately")
        finally:
            p.join()
