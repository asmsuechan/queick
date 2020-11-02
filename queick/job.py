import importlib
from concurrent.futures import ThreadPoolExecutor
import os
import traceback
import time
import pdb

from .constants import RETRY_TYPE
from .logger import logger

class Job:
    def __init__(self, func_name, args, scheduler, network_watcher, start_at=time.time(), priority=1,
                retry=False, retry_interval=10, max_retry_interval=600, retry_on_network_available=False,
                retry_type=RETRY_TYPE.CONSTANT, max_workers=os.cpu_count()):
        self.func_name = func_name
        self.args = args
        self.max_workers = max_workers
        self.scheduler = scheduler
        self.priority = priority
        self.retry = retry
        self.retry_interval = retry_interval
        self.max_retry_interval = max_retry_interval
        self.retry_type = retry_type
        self.start_at = start_at
        self.retry_on_network_available = retry_on_network_available
        self.retry_count = 0
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self.__minimum_retry_interval = 1

        f = self.__import_job_module(self.func_name)
        self.func = self.__create_func_with_error_handling(f)

        self.network_watcher = network_watcher

    def perform(self):
        self.__async_execute(self.func, self.args)

    def __async_execute(self, func, args):
        future = self.executor.submit(self.func, args)

    def terminate(self):
        self.executor.shutdown()

    def __create_func_with_error_handling(self, func):
        def f(args):
            try:
                func(*args)
            except Exception as e:
                # TODO: Fix this ugly error message
                error_msg = "Traceback (most recent call last):\n" + \
                        "".join(traceback.extract_tb(e.__traceback__).format()) + \
                        type(e).__name__ + ":" + str(e)
                logger.error(error_msg)
                if not self.retry_on_network_available and self.retry:
                    self.__schedule_retry()
                else:
                    # The priority of retry_on_network_available is higher than retry.
                    # Normal retry will be ignored when retry_on_network_available == True.
                    self.network_watcher.enqueue(self.__job_input_obj)

                self.terminate()
        return f

    @property
    def __job_input_obj(self):
        return {
                "func_name": self.func_name,
                "args": self.args,
                "retry": self.retry,
                "retry_interval": self.retry_interval,
                "retry_type": self.retry_type,
                "max_retry_interval": self.max_retry_interval,
                "retry_on_network_available": self.retry_on_network_available,
                "max_workers": self.max_workers
                }

    def __schedule_retry(self):
        self.__increase_retry_count()
        self.start_at = self.start_at + self.__calc_interval()
        self.scheduler.put(self)
        self.scheduler.run()

    def __increase_retry_count(self):
        self.retry_count += 1

    def __calc_interval(self):
        interval = self.__minimum_retry_interval
        if self.retry_type == RETRY_TYPE.CONSTANT:
            interval = self.retry_interval
        elif self.retry_type == RETRY_TYPE.COUNT_INCREASING:
            interval = self.retry_count
        elif self.retry_type == RETRY_TYPE.LINEAR_INCREASING:
            interval = self.retry_interval * self.retry_count

        if interval > self.max_retry_interval:
            interval = self.max_retry_interval

        return interval

    def __import_job_module(self, name):
        module_name, attribute = name.rsplit('.', 1)
        m = importlib.import_module(module_name)
        module = importlib.reload(m)
        return getattr(module, attribute)
