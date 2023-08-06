import unittest

from com.qxdzbc.p6.cell.Cells import Cells
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.cell.rpc_data_structure.CellId import CellId
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellValueProto, CellProto, CellContentProto


class Cells_test(unittest.TestCase):

    def test_FromProto2(self):
        address = CellAddresses.fromLabel("C23")

        proto = CellProto(
            id = CellId(
                cellAddress = address,
                wbKey = WorkbookKeys.fromNameAndPath("wb1"),
                wsName = "S1"
            ).toProtoObj(),
            content = CellContentProto(
                cellValue = CellValueProto(str = "123qwe"),
                formula = "formula z",
            )
        )

        cell = Cells.fromProto(proto)
        self.assertEqual(proto.id,cell.id.toProtoObj())