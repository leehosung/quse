import unittest
import sys
sys.path.insert(0, "..")
from quse import Quse
from datetime import datetime


class WeeklyTestCase(unittest.TestCase):

    def setUp(self):
        self.quse = Quse()

    def test_get_oneday_sleep_stat(self):
        (total_duration, deep_sleep_duration) =\
            self.quse.get_oneday_sleep_stat(datetime(2015, 2, 15))
        self.assertEqual(24120, total_duration)
        self.assertEqual(8880, deep_sleep_duration)


if __name__ == '__main__':
    unittest.main()
