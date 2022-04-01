import unittest

from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.address.CellAddressJson import CellAddressJson
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.communication.event.P6Events import P6Events
from bicp_document_structure.communication.P6Message import P6Message
from bicp_document_structure.communication.P6MessageHeader import P6MessageHeader
from bicp_document_structure.communication.proto.P6MsgProtos_pb2 import P6MessageProto


class P6MessageTest(unittest.TestCase):

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
            data =contentObj
        )

        expected = P6MessageProto()
        expected.ParseFromString(msg.toProtoBytes())
        self.assertEqual(msg.header.toProtoObj(),expected.header)