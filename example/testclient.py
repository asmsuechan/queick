from queick import JobQueue, RETRY_TYPE
from jobfunc import function, function2

q = JobQueue()
# q.enqueue(function, args=(1, 2,), retry_type=RETRY_TYPE.LINEAR_INCREASING)
q.enqueue(function, args=(1, 2,))
q.enqueue(function2, args=(1,))
# for i in range(0, 20):
#     q.enqueue(function, "aaaa")
