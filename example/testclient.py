from queick import JobQueue
from jobfunc import function

q = JobQueue()
q.enqueue(function, args=(1, 2,))
# for i in range(0, 20):
#     q.enqueue(function, "aaaa")
