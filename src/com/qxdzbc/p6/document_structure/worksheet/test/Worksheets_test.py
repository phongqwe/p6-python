import unittest
from unittest.mock import MagicMock

from com.qxdzbc.p6.document_structure.cell.address.CellAddressJson import CellAddressJson
from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.document_structure.worksheet.Worksheets import Worksheets
from com.qxdzbc.p6.proto.DocProtos_pb2 import WorksheetProto, CellProto, CellValueProto


class Worksheets_test(unittest.TestCase):
    pass
    # def test_FromProto(self):
        # wsProto = WorksheetProto()
        # wsProto.name = "Sheet1"
        #
        # a1 = CellProto()
        # a1.address.CopyFrom(CellAddresses.fromLabel("A1").toProtoObj())
        # a1.value.CopyFrom(CellValueProto(
        #     num=123
        # ))
        #
        # x12Proto = CellProto()
        #
        # x12Proto.address.CopyFrom(CellAddresses.fromLabel("X12").toProtoObj())
        # x12Proto.value.CopyFrom(CellValueProto(
        #     str="a string"
        # ))
        # x12Proto.formula = "formula x12"
        #
        # wsProto.cell.extend([
        #     a1, x12Proto
        # ])
        #
        # ws: Worksheet = Worksheets.fromProto(wsProto)
        # self.assertEqual(wsProto.name, ws.name)
        # self.assertTrue(ws.hasCellAt(CellAddresses.fromLabel("A1")))
        # self.assertTrue(ws.hasCellAt(CellAddresses.fromLabel("X12")))
        # self.assertEqual(2, len(ws.cells))
        # self.assertEqual(ws.name, ws.cell("A1").wsName)
        # self.assertEqual(ws.name, ws.cell("X12").wsName)


if __name__ == '__main__':
    unittest.main()
