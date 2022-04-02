import unittest

from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.Cells import Cells
from bicp_document_structure.cell.address.CellAddressJson import CellAddressJson


class Cells_test(unittest.TestCase):
    def test_CreateCellFromJson(self):
        cellJson = CellJson("value", "script", "formula", CellAddressJson(12, 33))
        cell = Cells.cellFromJson(cellJson)
        self.assertEqual(cellJson.value, cell.bareValue())
        self.assertEqual(cellJson.formula, cell.bareFormula())
        self.assertEqual(cellJson.script, cell.bareScript())

    def test_CreateCellFromJsonStr(self):
        cellJson = CellJson("value", "script", "formula", CellAddressJson(12, 33))
        cellJsonStr = str(cellJson)
        cell = Cells.cellFromJson(cellJsonStr)
        self.assertEqual(cellJson.value, cell.bareValue())
        self.assertEqual(cellJson.formula, cell.bareFormula())
        self.assertEqual(cellJson.script, cell.bareScript())