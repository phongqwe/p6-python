import unittest
from unittest.mock import MagicMock

from com.qxdzbc.p6.document_structure.cell.Cells import Cells
from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.new_architecture.rpc.data_structure.CellId import CellId
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellValueProto, Cell2Proto


class Cells_test(unittest.TestCase):

    def test_FromProto2(self):
        address = CellAddresses.fromLabel("C23")

        proto = Cell2Proto(
            id = CellId(
                cellAddress = address,
                wbKey = WorkbookKeys.fromNameAndPath("wb1"),
                wsName = "S1"
            ).toProtoObj(),
            value = CellValueProto(str="123qwe"),
            formula = "formula z",
        )

        cell = Cells.fromProto2(proto)
        self.assertEqual(proto.id,cell.id.toProtoObj())