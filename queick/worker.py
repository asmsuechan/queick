from multiprocessing import Process, Queue, Event
import socket
import pickle
import time
import importlib

from .queue_manager import QueueManager
from .scheduled_queue import ScheduledQueue

event = Event()

class Worker:
    # Start tcp server for listening new job arrival messages
    def listen_job(self, qm, sq):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 9999))
        s.listen(1)

        while True:
            conn, addr = s.accept()
            data = conn.recv(1024)
            if not data: break

            data_variable = pickle.loads(data)
            qm.enqueue(data_variable)
            event.set()

            print('data : {}, addr: {}'.format(data_variable, addr))
            conn.sendall(b'Received: ')
        conn.close()

    def watch_queue(self, qm, sq):
        event.wait()
        while True:
            while qm.is_empty() != True:
                data = qm.dequeue()

                job = qm.create_job(data['func_name'], data['args'], sq, retry_interval=data['retry_interval'], retry_type=data['retry_type'])
                job.perform()

                print(data)

            event.clear()
            if qm.is_empty():
              event.wait()

    def work(self):
        try:
            qm = QueueManager(queue_class=Queue)
            sq = ScheduledQueue()

            p = Process(target=self.listen_job, args=(qm, sq,))
            p.start()

            self.watch_queue(qm, sq)

        except KeyboardInterrupt:
            pass
        finally:
            p.join()
