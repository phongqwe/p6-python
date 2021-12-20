import unittest

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.worksheet.WorksheetImp import WorksheetImp


class TempCellTest(unittest.TestCase):
    def test_Cell(self):
        s = WorksheetImp()
        code = "x=1;y=x+2;y"
        eValue = 3
        address = CellIndex(1,1)

        # this is a TempCell
        c:Cell = s.getCell(address)
        self.assertTrue(s.isEmpty())

        c.code = code
        self.assertFalse(s.isEmpty())
        anotherC = s.getCell(address)
        self.assertEqual(code,c.code)
        self.assertEqual(code,anotherC.code)

        c.runCode()
        self.assertEqual(eValue,c.value)
        self.assertEqual(eValue,anotherC.value)

