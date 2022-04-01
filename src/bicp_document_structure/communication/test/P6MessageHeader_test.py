import unittest

from bicp_document_structure.communication.event.P6Events import P6Events
from bicp_document_structure.communication.P6MessageHeader import P6MessageHeader
from bicp_document_structure.communication.proto.P6MsgProtos_pb2 import P6MessageHeaderProto


class P6MessageHeaderTest(unittest.TestCase):
    def test_toJsonStr(self):
        hd=P6MessageHeader("id1", P6Events.Cell.UpdateValueEvent)
        protoObj = hd.toProtoObj()
        print(protoObj)
        self.assertEqual(hd.msgId,protoObj.msgId)
        self.assertEqual(P6Events.Cell.UpdateValueEvent.toProtoObj(),protoObj.eventType)