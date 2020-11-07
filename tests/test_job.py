import unittest
from concurrent.futures import ThreadPoolExecutor

from queick.job import Job
from queick.exceptions import NoSuchJobError

class TestJob(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_init(self):
        Job('tests.testfunc.func', ('test',), None, None, None)

    def test_init_error(self):
        with self.assertRaises(NoSuchJobError):
            j = Job('tests.notfound.func', ('test',), None, None, None)
            j.func

    def test_perform(self):
        executor = ThreadPoolExecutor(max_workers=1)
        job = Job('tests.testfunc.func_return_arg', ('test',), executor, None, None)
        future = job.perform()
        result = future.result()
        self.assertEqual(result, 'test')
