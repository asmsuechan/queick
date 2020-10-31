import socket
import pickle

from .constants import RETRY_TYPE

class JobQueue:
    def enqueue(self, func, args=None, priority=1, retry=True, retry_interval=10, max_retry_interval=600, retry_type=RETRY_TYPE.CONSTANT, max_workers=10):
        func_name = func.__module__ + "." + func.__name__
        payload = {
                "func_name": func_name,
                "args": args,
                "retry": retry,
                "retry_interval": retry_interval,
                "retry_type": retry_type,
                "max_retry_interval": max_retry_interval,
                "max_workers": max_workers
                }
        self.__send_to_job_listener(payload)

    def enqueue_at(self, start_at, func, args=None, priority=1, retry=True, retry_interval=10, max_retry_interval=600, retry_type=RETRY_TYPE.CONSTANT, max_workers=10):
        func_name = func.__module__ + "." + func.__name__
        payload = {
                "func_name": func_name,
                "start_at": start_at,
                "args": args,
                "retry": retry,
                "retry_interval": retry_interval,
                "retry_type": retry_type,
                "max_retry_interval": max_retry_interval,
                "max_workers": max_workers
                }
        self.__send_to_job_listener(payload)

    def __send_to_job_listener(self, payload):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9999))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.sendall(pickle.dumps(payload))

        msg = s.recv(1024)
        print(msg.decode("utf-8"))
