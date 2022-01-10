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
        c:Cell = s.getOrMakeCell(address)
        self.assertTrue(s.isEmpty())

        c.script = code
        self.assertFalse(s.isEmpty())
        anotherC = s.getOrMakeCell(address)
        self.assertEqual(code, c.script)
        self.assertEqual(code, anotherC.script)

        c.runScript()
        self.assertEqual(eValue,c.value)
        self.assertEqual(eValue,anotherC.value)

