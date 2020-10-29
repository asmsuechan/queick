import socket
import pickle

from .job import Job

class QueueManager:
    def __init__(self, queue_class=None):
        self.queue = queue_class()

    def enqueue(self, value):
        self.queue.put(value)

    def dequeue(self):
        return self.queue.get()

    def is_empty(self):
        return self.queue.empty()

    def create_job(self, *args, **kwargs):
        return Job(*args, **kwargs)
