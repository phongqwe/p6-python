import unittest


class Bench(unittest.TestCase):

    def f(self,n):
        if n>100:
            y = n-10
        else:
            x = self.f(n+11)
            y = self.f(x)
        return y
    def test_z(self):
        x = None
        print(isinstance(x,Exception))