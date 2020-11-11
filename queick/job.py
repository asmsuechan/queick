import importlib
import traceback
import time
from logging import getLogger
from random import random

from .constants import RETRY_TYPE, NW_STATE
from .exceptions import NoSuchJobError

from concurrent.futures import ThreadPoolExecutor, Future
from types import MethodType

logger = getLogger(__name__)


class Job:
    def __init__(
            self,
            func_name: str,
            args: tuple,
            executor: ThreadPoolExecutor,
            scheduler,
            network_watcher,
            start_at: float = time.time(),
            priority: int = 1,
            retry: bool = False,
            retry_interval: int = 10,
            max_retry_interval: int = 3600,
            retry_on_network_available: bool = False,
            retry_type=RETRY_TYPE.EXPONENTIAL):
        self.func_name = func_name
        self.args = args
        self.scheduler = scheduler
        self.priority = priority
        self.retry = retry
        self.retry_interval = retry_interval
        self.max_retry_interval = max_retry_interval
        self.retry_type = retry_type
        self.start_at = start_at
        self.retry_on_network_available = retry_on_network_available
        self.retry_count = 0
        self.executor = executor
        self._minimum_retry_interval = 1

        self.cron = False
        self.cron_interval = 0

        self.network_watcher = network_watcher

    @property
    def func(self) -> MethodType:
        f, err = self._import_job_module(self.func_name)
        if isinstance(err, ModuleNotFoundError):
            raise NoSuchJobError(
                'Queick worker could not find the job. Please check your worker\'s launching directory.')
        if err:
            raise err
        return self._create_func_with_error_handling(f)

    def perform(self) -> Future:
        return self._async_execute(self.func, self.args)

    def _async_execute(self, func, args) -> Future:
        return self.executor.submit(self.func, args)

    def terminate(self) -> None:
        self.executor.shutdown(wait=False)

    def _create_func_with_error_handling(self, func: MethodType):
        def f(args):
            try:
                if self.cron:
                    self._register_cron()
                res = func(*args)
                self.terminate()  # Terminate all idle threads
                return res
            except Exception as e:
                logger.error("Error during executing a job function: %s",
                             self.func_name, exc_info=True)

                if not self.retry_on_network_available and self.retry:
                    self._schedule_retry()

                if self.retry_on_network_available:
                    # The priority of retry_on_network_available is higher than retry.
                    # Normal retry will be ignored when
                    # retry_on_network_available == True.
                    if self.network_watcher.state == NW_STATE.INITIATED:
                        logger.error(
                            'func_name: %s, args: %s, retry_on_network_available is specified, but --ping-host is not set to Queick worker.',
                            self.func_name,
                            self.args)
                    else:
                        self.network_watcher.enqueue(self.job_input_obj)

                self.terminate()
                return None
        return f

    @property
    def job_input_obj(self) -> dict:
        return {
            "func_name": self.func_name,
            "args": self.args,
            "retry": self.retry,
            "retry_interval": self.retry_interval,
            "retry_type": self.retry_type,
            "max_retry_interval": self.max_retry_interval,
            "retry_on_network_available": self.retry_on_network_available
        }

    def _schedule_retry(self) -> None:
        self._increase_retry_count()
        self.start_at = self.start_at + self._calc_retry_interval()
        self.scheduler.put(self)
        self.scheduler.run()

    def _register_cron(self) -> None:
        self.start_at += self.cron_interval
        self.scheduler.put(self)

    def _increase_retry_count(self) -> None:
        self.retry_count += 1

    def _calc_retry_interval(self) -> int:
        interval = self._minimum_retry_interval

        if self.retry_type == RETRY_TYPE.CONSTANT:
            interval = self.retry_interval
        elif self.retry_type == RETRY_TYPE.COUNT_INCREASING:
            interval = self.retry_count
        elif self.retry_type == RETRY_TYPE.LINEAR_INCREASING:
            interval = self.retry_interval * self.retry_count
        elif self.retry_type == RETRY_TYPE.EXPONENTIAL:
            sleep_seconds = (2 ** (self.retry_count - 1)) * \
                (0.5 * (1 + random()))
            sleep_seconds = max([1, sleep_seconds])
            interval = sleep_seconds

        if self.max_retry_interval >= 0 and interval > self.max_retry_interval:
            interval = self.max_retry_interval

        return interval

    def _import_job_module(self, name):
        try:
            module_name, attribute = name.rsplit('.', 1)
            m = importlib.import_module(module_name)
            module = importlib.reload(m)
            return getattr(module, attribute), None
        except ModuleNotFoundError as e:
            return None, e
