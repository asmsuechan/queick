from queick import JobQueue, RETRY_TYPE
from jobfunc import function, function2
import time

q = JobQueue()
# print(q.enqueue(function2, args=(1,)))
# q.enqueue(function, args=(1, 2,), retry_type=RETRY_TYPE.LINEAR_INCREASING)
for i in range(0, 1000000):
    q.enqueue(function, args=(1, 2,), retry_on_network_available=True)
# print(q.enqueue(function, args=(1, 2,), retry_on_network_available=True))
# print(q.enqueue(function, args=(1, 2,), retry_on_network_available=True))
# print(q.enqueue(function2, args=(1,)))
# print(q.enqueue(function, args=(1, 2,), retry_on_network_available=True))
# print(q.enqueue(function, args=(1, 2,), retry_on_network_available=True))
# q.enqueue(function2, args=(1,))
# for i in range(0, 10000):
#     q.enqueue(function, args=(1, 2,))
# print(q.enqueue_at(time.time() + 5, function, args=(1, 2,)))
