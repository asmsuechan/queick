import socket
import pickle

from .constants import RETRY_TYPE, TCP_SERVER_HOST, TCP_SERVER_PORT
from .exceptions import WorkerNotFoundError
from .scheduling_time import SchedulingTime

from types import MethodType
from typing import Union, Tuple


class JobQueue:
    def enqueue(self,
                func: MethodType,
                args: Union[tuple,
                            None] = None,
                priority: int = 1,
                retry: bool = False,
                retry_interval: int = 10,
                max_retry_interval: int = 600,
                retry_on_network_available: bool = False,
                retry_type: RETRY_TYPE = RETRY_TYPE.EXPONENTIAL,
                max_workers: int = 10) -> dict:
        return self._create_request(
            func,
            args,
            priority,
            retry,
            retry_interval,
            max_retry_interval,
            retry_on_network_available,
            retry_type,
            max_workers)

    def enqueue_at(self,
                   start_at: Union[float, SchedulingTime],
                   func: MethodType,
                   args: Union[tuple,
                               None] = None,
                   priority: int = 1,
                   retry: bool = False,
                   retry_interval: int = 10,
                   max_retry_interval: int = 600,
                   retry_on_network_available: bool = False,
                   retry_type: RETRY_TYPE = RETRY_TYPE.EXPONENTIAL,
                   max_workers: int = 10) -> dict:

        if isinstance(start_at, SchedulingTime):
            _sa = start_at.start_at
        else:
            _sa = start_at

        return self._create_request(
            func,
            args,
            priority,
            retry,
            retry_interval,
            max_retry_interval,
            retry_on_network_available,
            retry_type,
            max_workers,
            start_at=_sa)

    def cron(self, st: SchedulingTime,
             func: MethodType,
             args: Union[tuple,
                         None] = None,
             priority: int = 1,
             retry: bool = False,
             retry_interval: int = 10,
             max_retry_interval: int = 600,
             retry_on_network_available: bool = False,
             retry_type: RETRY_TYPE = RETRY_TYPE.EXPONENTIAL,
             max_workers: int = 10) -> dict:
        st.validate()
        return self._create_request(
            func,
            args,
            priority,
            retry,
            retry_interval,
            max_retry_interval,
            retry_on_network_available,
            retry_type,
            max_workers,
            start_at=st.start_at,
            interval=st.interval)

    def _create_request(self,
                        func: MethodType,
                        args,
                        priority: int,
                        retry: bool,
                        retry_interval: int,
                        max_retry_interval: int,
                        retry_on_network_available: bool,
                        retry_type: RETRY_TYPE,
                        max_workers: int,
                        start_at: Union[float,
                                        None] = None,
                        interval: Union[float, None] = None):
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
        if start_at:
            payload.update({"start_at": start_at})
        if interval:
            payload.update({"interval": interval})
        result, error = self._send_to_job_listener(payload)
        if error:
            raise error
        return result

    def _send_to_job_listener(
            self, payload: dict) -> Tuple[Union[dict, None], Union[None, WorkerNotFoundError]]:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((TCP_SERVER_HOST, TCP_SERVER_PORT))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.sendall(pickle.dumps(payload))

            msg = s.recv(1024)
            return pickle.loads(msg), None
        except ConnectionRefusedError:
            self._print_client_error(
                'Queick worker is not found. Make sure you launched queick.')
            return None, WorkerNotFoundError()

    def _print_client_error(self, msg: str) -> None:
        print('\033[91m' + msg + '\033[0m')
