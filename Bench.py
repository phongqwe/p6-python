import unittest

x=123

def zsd():
    return 10
class Bench(unittest.TestCase):
    def test_z(self):
        try:
            raise ValueError("abc")
        except Exception as e:
            print(e)



