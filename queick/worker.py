from multiprocessing import Process, Queue, Event
import socket
import pickle
import time
import importlib

from .queue_manager import QueueManager
from .job_receiver import JobReceiver
from .scheduler import Scheduler
from .network_watcher import NetworkWatcher, STATE
from .logger import logger

class Worker:
    def work(self, args):
        try:
            event = Event()
            qm = QueueManager(queue_class=Queue)
            scheduler = Scheduler()

            jr = JobReceiver()
            p = Process(target=jr.listen, args=(event, qm,))
            p.start()

            nw = NetworkWatcher("", 0, queue_class=Queue)
            # Start NetworkWatcher only when --host argument is passed
            if args.host:
                port = args.port if args.port != None else 80
                nw.hostname = args.host
                nw.port = port
                nw.start()

            qm.watch(event, scheduler, nw)

        except KeyboardInterrupt:
            p.terminate()
            if nw.state != STATE.INITIATED: nw.terminate()
            for job in scheduler.queue.queue:
                scheduler.queue.cancel(job)
            logger.info("Stopping... Press Ctrl+C to exit immediately")
        finally:
            p.join()
