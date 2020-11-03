import unittest

from queick.job import Job

class TestJob(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_init(self):
        Job('tests.testfunc.func', ('test',), None, None)

    def test_init_error(self):
        with self.assertRaises(ModuleNotFoundError):
            Job('tests.notfound.func', ('test',), None, None)

    def test_perform(self):
        job = Job('tests.testfunc.func_return_arg', ('test',), None, None)
        future = job.perform()
        result = future.result()
        self.assertEqual(result, 'test')
