import unittest
import ast
from collections import namedtuple

class A:
    def __init__(self,x):
        self.x=x

class A2(A):
    def __init__(self, x, y):
        super().__init__(x)
        self.y=y
class Bench(unittest.TestCase):

    def test_Cell(self):
        a = A(123)
        a2 = A2(123,456)
        print(isinstance(a2,A2))



