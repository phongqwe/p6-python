import unittest
import ast
from collections import namedtuple

m1 = -123
class Bench(unittest.TestCase):

    def test_Cell(self):
        d = {1:"1v",2:"2v"}
        print(list(d.values()))



