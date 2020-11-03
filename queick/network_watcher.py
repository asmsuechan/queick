import socket
import time

from multiprocessing import Process, Queue

from .constants import enum
from .job import Job

STATE = enum(
    'State',
    CONNECTED='connected',
    DISCONNECTED='disconnected',
    INITIATED='initiated',
)

class NetworkWatcher:
    def __init__(self, hostname, port, queue_class=None):
        self.hostname = hostname
        self.port = port
        self.check_interval = 5
        self.state = STATE.INITIATED

        self.p = Process(target=self.watch)

        qc = queue_class or Queue
        self.failed_queue = qc()

    def enqueue(self, job):
        self.failed_queue.put(job)

    def dequeue(self):
        return self.failed_queue.get()

    def _is_connected(self):
        try:
            host = socket.gethostbyname(self.hostname)
            s = socket.create_connection((host, self.port), 2)
            s.close()
            return True
        except:
            pass
        return False

    def start(self):
        self.p.start()
        self.state = STATE.CONNECTED

    def terminate(self):
        self.p.terminate()

    def is_empty(self):
        return self.failed_queue.empty()

    def watch(self):
        while True:
            if self._is_connected():
                if self.state == STATE.DISCONNECTED:
                    while self.is_empty() != True:
                        # Dequeue all from failed queue and perform them
                        data = self.dequeue()
                        job = Job(data['func_name'], data['args'], None, self, retry=data['retry'], retry_interval=data['retry_interval'], retry_type=data['retry_type'], retry_on_network_available=data['retry_on_network_available'])
                        job.perform()
                self.state = STATE.CONNECTED
            else:
                self.state = STATE.DISCONNECTED
            time.sleep(self.check_interval)
