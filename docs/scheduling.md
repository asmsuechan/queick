# Scheduling
Scheduled job execution is available by using `q.enqueue_at()` method. The first argument of the method is the unix timestamp of the job to be executed.

```python
q = JobQueue()
q.enqueue_at(time.time() + 5, function, args=(1, 2,))
```

The job will be executed 5 seconds later.

## SchedulingTime class
Instead of unix timestamp, `SchedulingTime` object can be passed as the schedule time.

```python
st = SchedulingTime()
st.starting_from(time.time() + 10)
q.enqueue_at(st, function, args=(1, 2,))
```
