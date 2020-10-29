import socket
import pickle

from .constants import RETRY_TYPE

class JobQueue:
    def enqueue(self, func, arg, retry_interval=10, retry_type=RETRY_TYPE.CONSTANT):
        func_name = func.__module__ + "." + func.__name__
        payload = {
                "func_name": func_name,
                "arg": arg,
                "retry_interval": retry_interval,
                "retry_type": retry_type
                }

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9999))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.sendall(pickle.dumps(payload))

        msg = s.recv(1024)
        print(msg.decode("utf-8"))
