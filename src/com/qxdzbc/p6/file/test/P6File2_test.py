import unittest

from com.qxdzbc.p6.file.P6File2 import P6File2


class P6File2_test(unittest.TestCase):
    def test_toProto(self):
        v = P6File2(
            version = "v1",
            content = b'abc'
        )

        proto = v.toProtoObj()
        self.assertEqual(v.version,proto.version)
        self.assertEqual(v.content, proto.content)


if __name__ == '__main__':
    unittest.main()
