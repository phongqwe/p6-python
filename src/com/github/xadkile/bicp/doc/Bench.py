import unittest
import ast
from collections import namedtuple

m1 = -123
class Bench(unittest.TestCase):

    def test_Cell(self):
        Point = namedtuple('Point', ['x', 'y'])
        p = Point(11, y=22)
        print(p.y)



