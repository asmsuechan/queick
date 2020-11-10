class WorkerNotFoundError(Exception):
    pass


class NoSuchJobError(Exception):
    pass


class IntervalMustAboveZeroError(Exception):
    pass


class MustSetStartAtError(Exception):
    pass
