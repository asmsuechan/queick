import time

from .exceptions import IntervalMustAboveZeroError


class SchedulingTime:
    def __init__(self):
        self.interval = 600  # 10 minutes
        self.start_at = None

    def every(self, seconds=0, minutes=0, hours=0):
        self.interval = seconds + minutes * 60 + hours * 3600
        return self

    def starting_from(self, start_at):
        self.start_at = start_at
        return self

    def from_now(self):
        self.start_at = time.time()
        return self

    def validate(self):
        if self.interval <= 0:
            raise IntervalMustAboveZeroError(
                'The value of interval must be over 0.')
        elif self.start_at is None:
            raise MustSetStartAtError(
                'start_at have to be specified if starting_from() is used.')
