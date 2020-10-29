import importlib
from concurrent.futures import ThreadPoolExecutor
import traceback
import time
import pdb

from .constants import RETRY_TYPE

class Job:
    def __init__(self, func_name, arg, sq, priority=1, retry_interval=10, max_retry_interval=600, retry_type=RETRY_TYPE.CONSTANT, max_workers=10):
        self.func_name = func_name
        self.arg = arg
        self.max_workers = max_workers
        self.sq = sq
        self.priority = priority
        self.retry_interval = retry_interval
        self.max_retry_interval = max_retry_interval
        self.retry_type = retry_type
        self.start_at = time.time()
        self.retry_count = 0
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self.__minimum_retry_interval = 1

    @property
    def func(self):
        f = self.__import_job_module(self.func_name)
        return self.__create_func_with_error_handling(f)

    def perform(self):
        self.__async_execute(self.func, self.arg)

    def __async_execute(self, func, arg):
        future = self.executor.submit(self.func, arg)

    def terminate(self):
        self.executor.shutdown()

    def __create_func_with_error_handling(self, func):
        def f(arg):
            try:
                func(arg)
            except:
                traceback.print_exc()
                self.retry()
                self.terminate()
        return f

    def retry(self):
        try:
            self.__increase_retry_count()
            self.start_at = self.start_at + self.__calc_interval()
            self.sq.enqueue(self)
        except:
            traceback.print_exc()

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

    # 実行するモジュールを変更したらプロセスも再起動しなくてはならない。。。
    # 実行するモジュールはそれ単体で動けなければならない。
    def __import_job_module(self, name):
        pdb.set_trace()
        module_name, attribute = name.rsplit('.', 1)
        module = importlib.import_module(module_name)
        return getattr(module, attribute)