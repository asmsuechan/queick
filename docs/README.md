# How to use Queick
This document explains how to use queick practically.

## The simplest usage
First, queick worker is needed to be started.

```
$ queick
```

Here's the simplest example of a job execution in Python. It only displays 'hello' at queick worker's terminal after 1 second.

Most importantly, the job itself and the `enqueue` method must be written in separated files.

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
```

## Detailed usage
* [Retry](/docs/retry.md)
* [Retry on network available](/docs/retry_on_network_available.md)
* [Schedule](/docs/scheduling.md)
* [Run periodically (cron)](/docs/cron.md)
