from multiprocessing import Process, Queue, Event
import socket
import pickle
import time
import importlib

from .queue_manager import QueueManager
from .scheduler import Scheduler

event = Event()

class Worker:
    # Start tcp server for listening new job arrival messages
    def listen_job(self, qm, scheduler):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 9999))
        s.listen(1)

        while True:
            conn, addr = s.accept()
            data_bytes = conn.recv(1024)
            if not data_bytes: break

            data = pickle.loads(data_bytes)
            qm.enqueue(data)
            event.set()

            print('data : {}, addr: {}'.format(data, addr))
            conn.sendall(b'Received: ')
        conn.close()

    def watch_queue(self, qm, scheduler):
        event.wait()
        while True:
            while qm.is_empty() != True:
                data = qm.dequeue()

                job = qm.create_job(data['func_name'], data['args'], scheduler, retry=data['retry'], retry_interval=data['retry_interval'], retry_type=data['retry_type'])
                if 'start_at' in data:
                    job.start_at = data['start_at']
                    scheduler.put(job)
                    scheduler.run()
                else:
                    job.perform()

                print(data)

            event.clear()
            if qm.is_empty():
              event.wait()

    def work(self):
        try:
            qm = QueueManager(queue_class=Queue)
            scheduler = Scheduler()

            p = Process(target=self.listen_job, args=(qm, scheduler,))
            p.start()

            self.watch_queue(qm, scheduler)

        except KeyboardInterrupt:
            p.terminate()
            for job in scheduler.queue.queue:
                scheduler.queue.cancel(job)
            print("Stopping... Press Ctrl+C to exit immediately")
        finally:
            p.join()
