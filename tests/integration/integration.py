from queick import JobQueue, RETRY_TYPE
from jobfunc import function
import time

def file_line_length(path):
    with open(path) as f:
        l = f.readlines()
    return len(l)

path = 'testfile'

q = JobQueue()

with open(path, mode='w') as f:
    f.write("")

initial_length = file_line_length(path)
q.enqueue(function, args=(path, "first line\n",))
time.sleep(1)
first_length = file_line_length(path)

assert first_length - initial_length == 1, "1 line must be added"

q.enqueue_at(time.time() + 4, function, args=(path, "second line\n",))
pre_second_length = file_line_length(path)

assert pre_second_length == first_length, "Job must be scheduled"

time.sleep(5)
second_length = file_line_length(path)
assert second_length - pre_second_length == 1, "Job must be executed after 4 seconds"
