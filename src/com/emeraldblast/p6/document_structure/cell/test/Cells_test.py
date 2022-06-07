import unittest

from com.emeraldblast.p6.document_structure.cell.CellJson import CellJson
from com.emeraldblast.p6.document_structure.cell.Cells import Cells
from com.emeraldblast.p6.document_structure.cell.address.CellAddressJson import CellAddressJson
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.proto.DocProtos_pb2 import CellProto


class Cells_test(unittest.TestCase):

    def test_FromProto2(self):
        address = CellAddresses.fromLabel("@C23")

        proto = CellProto(
            address = address.toProtoObj(),
            value = "123qwe",
            formula = "formula z",
            isFormula = True,
        )

        cell = Cells.fromProto(proto)
        self.assertEqual(address, cell.address)
        self.assertEqual(proto.formula, cell.formula)
        self.assertEqual(proto.value, cell.bareValue)

    def test_FromProto(self):
        address = CellAddresses.fromLabel("@C23")

        proto = CellProto()
        proto.address.CopyFrom(address.toProtoObj())
        proto.value="123"
        proto.formula= "formula z"
        proto.isFormula = True

        cell = Cells.fromProto(proto)
        self.assertEqual(address,cell.address)
        self.assertEqual(proto.formula,cell.bareFormula)
        self.assertEqual("123", cell.bareValue)

    def test_CreateCellFromJson(self):
        cellJson = CellJson("value", "script", "formula", CellAddressJson(12, 33))
        cell = Cells.cellFromJson(cellJson)
        self.assertEqual(cellJson.value, cell.bareValue)
        self.assertEqual(cellJson.formula, cell.bareFormula)
        self.assertEqual(cellJson.script, cell.bareScript)

    def test_CreateCellFromJsonStr(self):
        cellJson = CellJson("value", "script", "formula", CellAddressJson(12, 33))
        cellJsonStr = str(cellJson)
        cell = Cells.cellFromJson(cellJsonStr)
        self.assertEqual(cellJson.value, cell.bareValue)
        self.assertEqual(cellJson.formula, cell.bareFormula)
        self.assertEqual(cellJson.script, cell.bareScript)