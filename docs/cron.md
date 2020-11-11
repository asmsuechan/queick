# Cron (periodical execution)
A job can be run in the background and on a schedule by using `q.cron()` method.

```python
st = SchedulingTime()
st.every(minutes=1).starting_from(time.time() + 10)
q.cron(st, function, args=(1, 2,))
```

This job will be executed 10 seconds later and every 1 minute.

Also, running **every midnight** is supported by `st.from_midnight()` method. It sets `start_at` to the day's midnight.

```python
st = SchedulingTime()
st.every(days=1).from_midnight()
q.cron(st, function, args=(1, 2,))
```
