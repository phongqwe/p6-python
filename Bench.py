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
        for n in range(-1000,1000):
            # if n<=100:
            #     ret = self.f(n)
            #     self.assertEqual(91,ret)

            ret = self.f(n)
            self.assertTrue(ret>=91)

            # if n>=100:
            #     ret = self.f(n)
            #     self.assertTrue(n-10,ret)

            # ret = self.f(n)
            # z1 = (not n<=100) or (ret == 91)
            # z2 = (not n>100) or (ret == n-10)
            # self.assertTrue(z1 and z2)
