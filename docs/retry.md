# Retry
A job can be retried when it raises an error. `retry=True` option must be passed to `enqueue()` method to use this feature.

```python
q = JobQueue()
q.enqueue(function, args=(1, 2,), retry=True)
```

## Retry interval
The default retry algorithm is [exponential backoff](https://en.wikipedia.org/wiki/Exponential_backoff). 3 types of algorithms are prepared other than exponential backoff.

* Constant interval
* Linear increasing
* Count increasing

Even if an interval continuously increases, the value is up to `max_retry_interval`. If you do not set the maximum value, you have to set `max_retry_interval=-1`.

<!-- if an interval exceeds `max_retry_interval`, the interval becomes `max_retry_interval`. -->

## Constant interval
A failed job will be executed **every fixed seconds** (10 seconds for default).

```python
from queick import RETRY_TYPE
q = JobQueue()
q.enqueue(function, args=(1, 2,), retry=True, retry_type=RETRY_TYPE.CONSTANT, retry_interval=60)
```

If you do not pass `retry_interval` option, 10 second is set to the value by default.

## Linear increasing
The interval increases in a linear way. It is calculated by multiplying `retry_interval` with the repeat count.

```python
from queick import RETRY_TYPE
q = JobQueue()
q.enqueue(function, args=(1, 2,), retry=True, retry_type=RETRY_TYPE.LINEAR_INCREASING, retry_interval=10)
```

The first failure's interval is `10 * 1 = 10 seconds`, the second is `10 * 2 = 20 seconds`, the third is `10 * 3 = 30 seconds`, and so on.

## Count increasing
The interval is the failure count of a job.

```python
from queick import RETRY_TYPE
q = JobQueue()
q.enqueue(function, args=(1, 2,), retry=True, retry_type=RETRY_TYPE.COUNT_INCREASING)
```

The first failure's interval is 1 second, the second is 2 seconds, the third is 3 seconds and so on.
