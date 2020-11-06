import unittest
import time

from queick.queue_manager import QueueManager
from queick.job import Job

class TestQueueManager(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_enqueue(self):
        qm = QueueManager()
        qm.enqueue({ 'test': 'test' })
        time.sleep(0.01) # Wait until enqueue finishes
        self.assertEqual(qm.queue.qsize(), 1)
        qm.dequeue()

    def test_dequeue(self):
        qm = QueueManager()
        qm.enqueue({ 'test': 'test' })
        time.sleep(0.01) # Wait until enqueue finishes
        val = qm.dequeue()
        self.assertEqual(val['test'], 'test')

    def test_is_empty(self):
        qm = QueueManager()
        self.assertEqual(qm.is_empty(), True)
        qm.enqueue({ 'test': 'test' })
        time.sleep(0.01) # Wait until enqueue finishes
        self.assertEqual(qm.is_empty(), False)

    def test_create_job(self):
        qm = QueueManager()
        job = qm.create_job('tests.testfunc.func', ('test',), None, None, None)
        self.assertEqual(type(job), Job)
