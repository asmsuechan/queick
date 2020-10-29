# Queick
The simple inmemory job-queue manager.

## Feature
* Written in Python
* Job-queue manager **without redis**
* Working for low-spec machines

## Installation
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

q = JobQueue()
q.enqueue(function, "hello")
```

```
$ python jobfunc.py
```
