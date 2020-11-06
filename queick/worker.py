from multiprocessing import Process, Queue, Event
import socket
import pickle
import time
import importlib
import sys
from logging import DEBUG, INFO, getLogger

from .constants import NW_STATE
from .queue_manager import QueueManager
from .job_receiver import JobReceiver
from .scheduler import Scheduler
from .network_watcher import NetworkWatcher
from .logger import setup_logger

logger = getLogger(__name__)

class Worker:
    def work(self, ping_host=None, ping_port=80, log_filepath=None, debug=False):
        loglevel = DEBUG if debug else INFO
        setup_logger(loglevel=loglevel, filepath=log_filepath)
        sys.path.append('.')
        logger.info('Welcome to Queick!')

        try:
            event = Event()
            qm = QueueManager(queue_class=Queue)
            scheduler = Scheduler()

            jr = JobReceiver()
            p = Process(target=jr.listen, args=(event, qm,))
            p.start()

            nw = NetworkWatcher("", 0, queue_class=Queue)
            # Start NetworkWatcher only when --ping-host argument is passed
            if ping_host:
                nw.hostname = ping_host
                nw.port = ping_port
                nw.start()

            qm.watch(event, scheduler, nw)

        except KeyboardInterrupt:
            p.terminate()
            if nw.state != NW_STATE.INITIATED: nw.terminate()
            for job in scheduler.queue.queue:
                scheduler.queue.cancel(job)
            logger.info("Stopping... Press Ctrl+C to exit immediately")
        finally:
            p.join()
