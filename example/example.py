from queick import JobQueue, RETRY_TYPE
from jobfunc import function
import time

q = JobQueue()
q.enqueue(function, args=(1, 2,))
q.enqueue_at(time.time() + 5, function2, args=(2, 3,))

st = SchedulingTime()
st.every(minutes=1).starting_from(time.time() + 10)
q.cron(st, function, args=(1, 2,))
