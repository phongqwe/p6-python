import unittest

from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.address.CellAddressJson import CellAddressJson
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.message.event.P6Events import P6Events
from bicp_document_structure.message.P6Message import P6Message
from bicp_document_structure.message.P6MessageHeader import P6MessageHeader
from bicp_document_structure.message.proto.P6MsgPM_pb2 import P6MessageProto


class P6MessageTest(unittest.TestCase):
    def test_toRawMsg(self):
        contentObj = CellJson(
            value="cell value",
            script="cell script",
            formula="=1234",
            address=CellAddressJson(1, 34)
        )
        hd = P6MessageHeader("id1", P6Events.Cell.UpdateValueEvent)
        msg = P6Message(
            header=hd,
            content=contentObj
        )
        jsonStr = msg.toJsonStr()
        expectaction = """{"header": {"msgId": "id1", "eventType": "cell_value_update"}, "content": {"data": "{\\\"value\\\": \\\"cell value\\\", \\\"script\\\": \\\"cell script\\\", \\\"formula\\\": \\\"=1234\\\", \\\"address\\\": {\\\"row\\\": 34, \\\"col\\\": 1}}"}}"""
        self.assertEqual(expectaction, jsonStr)
        self.assertEqual(bytes(expectaction.encode("UTF-8")),msg.toBytes())

    def test_toProtoBytes(self):
        contentObj = DataCell(
            value="cell value",
            script="cell script",
            formula="=1234",
            address=CellIndex(1, 34)
        )
        hd = P6MessageHeader("id1", P6Events.Cell.UpdateValueEvent)
        msg = P6Message(
            header=hd,
            content=contentObj
        )

        expected = P6MessageProto()
        expected.ParseFromString(msg.toProtoBytes())
        self.assertEqual(msg.header.toProtoObj(),expected.header)
        self.assertEqual(contentObj.toProtoStr(),expected.data)