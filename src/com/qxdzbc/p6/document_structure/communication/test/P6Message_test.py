import unittest

from com.qxdzbc.p6.document_structure.cell.DataCell import DataCell
from com.qxdzbc.p6.document_structure.cell.address.CellIndex import CellIndex
from com.qxdzbc.p6.document_structure.communication.event.P6Events import P6Events
from com.qxdzbc.p6.document_structure.communication.event_server.msg.P6Message import P6Message
from com.qxdzbc.p6.document_structure.communication.event_server.msg.P6MessageHeader import P6MessageHeader
from com.qxdzbc.p6.proto.P6MsgProtos_pb2 import P6MessageProto


class P6MessageTest(unittest.TestCase):

    def test_toProtoBytes(self):
        contentObj = DataCell(
            value="cell value",
            script="cell script",
            formula="=1234",
            address=CellIndex(1, 34)
        )
        hd = P6MessageHeader("id1", P6Events.Cell.Update.event)
        msg = P6Message(
            header=hd,
            data =contentObj
        )

        expected = P6MessageProto()
        expected.ParseFromString(msg.toProtoBytes())
        self.assertEqual(msg.header.toProtoObj(),expected.header)