import unittest


class Bench(unittest.TestCase):
    def test_z(self):
        d = {
            1:"1"
        }
        l = ["ab","c"]
        del(l[0])
        print(l)


