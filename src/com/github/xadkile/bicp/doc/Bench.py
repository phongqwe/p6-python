import unittest
from collections import OrderedDict


class A:
    def __init__(self,x):
        self.x=x

class A2(A):
    def __init__(self, x, y):
        super().__init__(x)
        self.y=y
class Bench(unittest.TestCase):

    def test_Cell(self):
        od = OrderedDict()
        od[1]="1v"
        od[2]="2v"




