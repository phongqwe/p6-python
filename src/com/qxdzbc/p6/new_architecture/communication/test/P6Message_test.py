import unittest

from com.qxdzbc.p6.new_architecture.communication import P6Events
from com.qxdzbc.p6.new_architecture.communication.msg import P6MessageHeader
from com.qxdzbc.p6.new_architecture.communication.msg.P6Message import P6Message
from com.qxdzbc.p6.proto.P6MsgProtos_pb2 import P6MessageProto


class P6MessageTest(unittest.TestCase):

    def test_toProtoBytes(self):
        hd = P6MessageHeader("id1", P6Events.Cell.Update.event)
        msg = P6Message(
            header=hd,
            data ="contentObj"
        )

        expected = P6MessageProto()
        expected.ParseFromString(msg.toProtoBytes())
        self.assertEqual(msg.header.toProtoObj(),expected.header)