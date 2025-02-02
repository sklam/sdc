import os
import unittest

from sdc.tests.tests_perf.test_perf_utils import *


class TestBase(unittest.TestCase):
    iter_number = 5

    @classmethod
    def setUpClass(cls):
        cls.test_results = TestResults()
        if is_true(os.environ.get('LOAD_PREV_RESULTS')):
            cls.test_results.load()

        cls.total_data_length = []
        cls.num_threads = int(os.environ.get('NUMBA_NUM_THREADS', config.NUMBA_NUM_THREADS))
        cls.threading_layer = os.environ.get('NUMBA_THREADING_LAYER', config.THREADING_LAYER)

    @classmethod
    def tearDownClass(cls):
        cls.test_results.print()
        cls.test_results.dump()
