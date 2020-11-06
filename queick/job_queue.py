import socket
import pickle

from .constants import RETRY_TYPE, TCP_SERVER_HOST, TCP_SERVER_PORT
from .exceptions import WorkerNotFoundError

class JobQueue:
    def enqueue(self, func, args=None, priority=1, retry=False, retry_interval=10,
                max_retry_interval=600, retry_on_network_available=False, retry_type=RETRY_TYPE.EXPONENTIAL, max_workers=10):
        return self._create_request(func, args, priority, retry, retry_interval,
                max_retry_interval, retry_on_network_available, retry_type, max_workers)

    def enqueue_at(self, start_at, func, args=None, priority=1,
                retry=False, retry_interval=10, max_retry_interval=600, retry_on_network_available=False,
                retry_type=RETRY_TYPE.EXPONENTIAL, max_workers=10):
        return self._create_request(func, args, priority, retry, retry_interval,
                max_retry_interval, retry_on_network_available, retry_type, max_workers, start_at=start_at)

    def _create_request(self, func, args, priority, retry, retry_interval,
                max_retry_interval, retry_on_network_available, retry_type, max_workers, start_at=None):
        func_name = func.__module__ + "." + func.__name__
        payload = {
                "func_name": func_name,
                "args": args,
                "retry": retry,
                "retry_interval": retry_interval,
                "retry_type": retry_type,
                "max_retry_interval": max_retry_interval,
                "retry_on_network_available": retry_on_network_available,
                "max_workers": max_workers
                }
        if start_at: payload.update({ "start_at": start_at })
        result, error = self._send_to_job_listener(payload)
        if error != None:
            raise error
        return result

    def _send_to_job_listener(self, payload):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((TCP_SERVER_HOST, TCP_SERVER_PORT))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.sendall(pickle.dumps(payload))

            msg = s.recv(1024)
            return pickle.loads(msg), None
        except ConnectionRefusedError:
            self._print_client_error('Queick worker is not found. Make sure you launched queick.')
            return None, WorkerNotFoundError()

    def _print_client_error(self, msg):
        print('\033[91m' + msg + '\033[0m')
