import unittest

from com.qxdzbc.p6.new_architecture.communication.msg.P6Event import P6Event
from com.qxdzbc.p6.new_architecture.communication.msg.P6MessageHeader import P6MessageHeader


class P6MessageHeaderTest(unittest.TestCase):
    def test_toJsonStr(self):
        hd= P6MessageHeader("id1", P6Event("e1","event 1"))
        protoObj = hd.toProtoObj()
        print(protoObj)
        self.assertEqual(hd.msgId,protoObj.msgId)
        self.assertEqual(P6Event("e1","event 1").toProtoObj(),protoObj.eventType)