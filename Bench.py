import re
import unittest

x=123

def zsd():
    return 10
class Bench(unittest.TestCase):
    def test_z(self):
        labelPattern = re.compile("@[A-Za-z]+[1-9][0-9]*")
        print(str(labelPattern.pattern))



