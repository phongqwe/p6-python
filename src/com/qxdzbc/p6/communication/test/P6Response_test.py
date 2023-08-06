import unittest

from com.qxdzbc.p6.communication.msg.P6MessageHeader import P6MessageHeader
from com.qxdzbc.p6.communication.msg.P6Event import P6Event
from com.qxdzbc.p6.communication.response.P6Response import P6Response


class P6Response_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.r = P6Response(
            header = P6MessageHeader("id", P6Event("e1","event 1")),
            data = b"data 123",
            status = P6Response.Status.OK
        )

    def test_toProto(self):
        proto = self.r.toProtoObj()


if __name__ == '__main__':
    unittest.main()
