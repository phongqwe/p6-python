import unittest
from unittest.mock import MagicMock

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.DataCell import DataCell
from com.emeraldblast.p6.document_structure.cell.WriteBackCell import WriteBackCell
from com.emeraldblast.p6.document_structure.cell.address.CellIndex import CellIndex
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp


class WriteBackCellTest(unittest.TestCase):

    def test_toProtoObj(self):
        c1 = DataCell(CellIndex(1, 1),
                      123)
        writeBackCell = WriteBackCell(c1,MagicMock())
        self.assertEqual(c1.toProtoObj(),writeBackCell.toProtoObj())

    def test_Cell(self):
        w = WorkbookImp("w")
        s = w.createNewWorksheet("s3")

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
        wb = WorkbookImp("wb")
        cellContainer = wb.createNewWorksheet("Sheet1")
        address = CellIndex(1, 1)
        c = WriteBackCell(cellContainer.cell(address),cellContainer)
        self.assertFalse(cellContainer.hasCellAt(address))

        # cell is added when script is changed
        c.script = "x=10;x+1;"
        self.assertTrue(cellContainer.hasCellAt(address))
        cellContainer.deleteCell(address)

        # cell is added when value is changed
        c.value = 123
        self.assertTrue(cellContainer.hasCellAt(address))
        cellContainer.deleteCell(address)

        # cell is added when setScriptAndRun is called
        c.setScriptAndRun("y=10;y+100;",globals())
        self.assertTrue(cellContainer.hasCellAt(address))
        cellContainer.deleteCell(address)

        # cell is add when new formula is set
        c.formula="zzbd"
        self.assertTrue(cellContainer.hasCellAt(address))
        cellContainer.deleteCell(address)