import unittest
from datetime import datetime

import time
class Bench(unittest.TestCase):
    def test_z(self):
        print(type(time.time()))