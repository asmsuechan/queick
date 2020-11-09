import socket
import time
from multiprocessing import Process, Queue
from logging import INFO, getLogger

from .constants import NW_STATE
from .job import Job

logger = getLogger(__name__)


class NetworkWatcher:
    def __init__(self, hostname, port, queue_class=None):
        self.hostname = hostname
        self.port = port
        self.check_interval = 1
        self.state = NW_STATE.INITIATED

        self.p = Process(target=self.watch)

        qc = queue_class or Queue
        self.failed_queue = qc()

    def enqueue(self, job):
        logger.debug('[NetworkWatcher] Job is queued: %s', job)
        self.failed_queue.put(job)

    def dequeue(self):
        return self.failed_queue.get()

    def _is_connected(self):
        logger.debug('[NetworkWatcher] Checking connection...')
        try:
            host = socket.gethostbyname(self.hostname)
            s = socket.create_connection((host, self.port), 2)
            s.close()
            return True
        except BaseException:
            pass
        return False

    def start(self):
        self.p.start()
        self.state = NW_STATE.CONNECTED

    def terminate(self):
        self.p.terminate()

    def is_empty(self):
        return self.failed_queue.empty()

    def watch(self):
        while True:
            if self._is_connected():
                if self.state == NW_STATE.DISCONNECTED:
                    while self.is_empty() != True:
                        # Dequeue all from failed queue and perform them
                        data = self.dequeue()
                        logger.debug(
                            '[NetworkWatcher] Job is dequeued: %s', data)
                        job = Job(
                            data['func_name'],
                            data['args'],
                            None,
                            self,
                            retry=data['retry'],
                            retry_interval=data['retry_interval'],
                            retry_type=data['retry_type'],
                            retry_on_network_available=data['retry_on_network_available'])
                        job.perform()
                self.state = NW_STATE.CONNECTED
            else:
                self.state = NW_STATE.DISCONNECTED
            time.sleep(self.check_interval)
