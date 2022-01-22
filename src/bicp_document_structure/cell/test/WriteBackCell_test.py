import unittest

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.WriteBackCell import WriteBackCell
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.cell.test.MockContainer import MockContainer
from bicp_document_structure.worksheet.WorksheetImp import WorksheetImp


class WriteBackCellTest(unittest.TestCase):
    def test_Cell(self):
        s = WorksheetImp()
        code = "x=1;y=x+2;y"
        eValue = 3
        address = CellIndex(1, 1)

        # this is a WriteBackCell
        c: Cell = s.getOrMakeCell(address)
        self.assertTrue(s.isEmpty())

        c.script = code
        self.assertFalse(s.isEmpty())
        anotherC = s.getOrMakeCell(address)
        self.assertEqual(code, c.script)
        self.assertEqual(code, anotherC.script)

        c.runScript(globals())
        self.assertEqual(eValue, c.value)
        self.assertEqual(eValue, anotherC.value)

    def test_wbCell(self):
        container = MockContainer()
        address = CellIndex(1, 1)
        c = WriteBackCell(DataCell(address), container)
        self.assertFalse(container.hasCellAt(address))

        # cell is added when script is changed
        c.script = "x=10;x+1;"
        self.assertTrue(container.hasCellAt(address))
        container.removeCell(address)

        # cell is added when value is changed
        c.value = 123
        self.assertTrue(container.hasCellAt(address))
        container.removeCell(address)

        # cell is added when setScriptAndRun is called
        c.setScriptAndRun("y=10;y+100;",globals())
        self.assertTrue(container.hasCellAt(address))
        container.removeCell(address)

        # cell is add when new formula is set
        c.formula="zzbd"
        self.assertTrue(container.hasCellAt(address))
        container.removeCell(address)
