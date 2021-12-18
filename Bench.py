import unittest
from collections import OrderedDict


class Bench(unittest.TestCase):
    def test_z(self):
        d = OrderedDict()
        d[1]="1v"
        d[2]="2v"
        del d[1]
        print(d)