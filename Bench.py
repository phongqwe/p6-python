import unittest
from functools import partial


class Bench(unittest.TestCase):

    def f1(self,x,y):
        print(y)
        return x+y
    def test_z(self):

        f11= partial(self.f1,y=33)
        print(f11(100))


