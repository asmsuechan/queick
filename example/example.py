from queick import JobQueue, RETRY_TYPE
from jobfunc import function, function2
import time

q = JobQueue()
q.enqueue(function2, args=('Normal job',))
q.enqueue_at(time.time() + 5, function2, args=('Scheduled job',))
