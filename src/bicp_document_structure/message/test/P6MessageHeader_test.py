import unittest

from bicp_document_structure.event.P6Events import P6Events
from bicp_document_structure.message.P6MessageHeader import P6MessageHeader
from bicp_document_structure.message.proto.P6MsgPM_pb2 import P6MessageHeaderProto


class P6MessageHeaderTest(unittest.TestCase):
    def test_toJsonStr(self):
        hd=P6MessageHeader("id1", P6Events.Cell.UpdateValue)
        print(hd.toJsonStr())
        self.assertEqual("""{"msgId": "id1", "eventType": "cell_value_update"}""",hd.toJsonStr())

    def test_toProtoStr(self):
        hd = P6MessageHeader("id1", P6Events.Cell.UpdateValue)
        print(hd.toProtoStr())
        expected = P6MessageHeaderProto()
        expected.ParseFromString(hd.toProtoBytes())
        self.assertEqual(hd.msgId,expected.msgId)
        self.assertEqual(hd.eventType.msgRepresentation,expected.eventType)