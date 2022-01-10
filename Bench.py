import unittest

x=123

def zsd():
    return 10

def execz(f):
    print(f())
class Bench(unittest.TestCase):
    def test_z(self):
        f = lambda : 2032
        execz(f)


