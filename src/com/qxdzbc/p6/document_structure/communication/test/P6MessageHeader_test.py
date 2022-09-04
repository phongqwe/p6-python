import unittest

from com.qxdzbc.p6.document_structure.communication.event.P6Events import P6Events
from com.qxdzbc.p6.document_structure.communication.event_server.msg.P6MessageHeader import P6MessageHeader


class P6MessageHeaderTest(unittest.TestCase):
    def test_toJsonStr(self):
        hd=P6MessageHeader("id1", P6Events.Cell.Update.event)
        protoObj = hd.toProtoObj()
        print(protoObj)
        self.assertEqual(hd.msgId,protoObj.msgId)
        self.assertEqual(P6Events.Cell.Update.event.toProtoObj(),protoObj.eventType)