# Queick
A simple inmemory job-queue manager for Python.

![capture](/capture.gif)

## Feature
* Written in Python only standard libraries
* Job-queue manager **without redis**
* Working for low-spec machines
* Retry
* **Retry on network available**
* Scheduling

## Installation
Python version >= 3.6 is required.

```
pip install queick
```

## Usage
First, launch queick worker.

```
$ queick
```

Second, prepare a job file (jobfunc.py) and an application (test.py).

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

Third, run the application.

```
$ python test.py
```

## Retry on network available
Jobs inside the **failed queue** will be dequeued when the network status changes from disconnected to connected.

Some setups are needed to use the retry mode. First, launch queick worker with --ping-host options (details below).

```
$ queick --ping-host asmsuechan.com # Please prepare your own ping server, do not use this.
```

Second, pass an option to the method.

```python
q.enqueue(function, args=("hello",), retry_on_network_available=True)
```

## Options
There are some options for queick worker.

|name|default|description|
|:-|-:|-:|
|-debug|False|if set, detailed logs will be shown|
|--ping-host <HOST>|None|hostname for NetworkWatcher to check if the machine has the internet connection|
|--ping-port <PORT>|80|port number for NetworkWatcher|
|--log-filepath <filepath>|None|logfile to save all the worker log|

An example usage is below:

```
$ queick -debug --ping-host asmsuechan.com
```

## Testing
Unit test:

```
$ python -m unittest
```

Integration test:

```
$ docker build -t queick-test .
$ docker run --rm -it queick-test:latest
```

## Development
Build queick for development.

```
$ python setup.py develop
```

## Deployment
Deployed at https://pypi.org/project/queick/.

```
$ python setup.py sdist
$ twine upload dist/*
```
