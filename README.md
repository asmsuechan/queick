# Queick
A simple inmemory job-queue manager.

![capture](/capture.gif)

## Feature
* Written in Python
* Job-queue manager **without redis**
* Working for low-spec machines

## Installation
Python version >= 3.6 is required.

```
pip install queick
```

## Usage
```
$ queick
```

```python
# jobfunc.py
import time
def function(arg):
    time.sleep(1)
    print(arg)

# test.py
from queick import JobQueue
from jobfunc import function
from time import time

q = JobQueue()
q.enqueue(function, args=("hello",))
q.enqueue_at(time() + 5, function, args=("world",)) # Run after 5 seconds
```

```
$ python jobfunc.py
```
