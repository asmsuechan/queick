# Retry on network available
The feature that is executing retry when the network connection is back is implemented because the main target is low-spec machines, such as Raspberry Pi, for IoT use cases of which the network environment is not powerful.

To use this feature, `--ping-host` option is needed to be passed on the worker's launch.

```bash
$ queick --ping-host examplehost.com
```

Then, enqueue a job with `retry_on_network_available=True` option.

```python
q = JobQueue()
q.enqueue(function, args=("hello",), retry_on_network_available=True)
```

## Architecture
NetworkWatcher watches the network connection every 1 second. And when the connection is unavailable, the state is set as `DISCONNECTED`. Also, if a job is executed during the `DISCONNECTED` state, it is enqueued in the **failed queue**. Then, the contents of the queue will be executed after NetworkWatcher confirms the network connection.

## See also
* [Retry](/docs/retry.md)
