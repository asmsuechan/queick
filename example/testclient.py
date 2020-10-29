from queick import JobQueue
from jobfunc import function

q = JobQueue()
q.enqueue(function, "aaaa")
# for i in range(0, 20):
#     q.enqueue(function, "aaaa")
