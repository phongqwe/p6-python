import unittest


class Bench(unittest.TestCase):
    def test_z(self):
        a = "abc"
        print(bytes(a.encode(encoding="UTF-8")))
