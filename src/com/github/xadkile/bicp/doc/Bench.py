import unittest

class Bench(unittest.TestCase):
    def test_Cell(self):
        d = dict()
        d["a"]=123
        d[2]=456
        print(d[2])
        print(d["a"])