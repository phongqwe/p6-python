import random
import unittest

from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.column.ColumnImp import ColumnImp
from bicp_document_structure.sheet.WorksheetImp import WorksheetImp


class WorksheetTest(unittest.TestCase):
    def makeTestObj(self):
        cellAddr = CellIndex(random.randrange(1, 20), random.randrange(1, 20))
        cell = DataCell(cellAddr, 123, "code")
        return cell, cellAddr

    def test_hasCellAt(self):
        s = WorksheetImp()
        self.assertFalse(s.hasCellAt(CellIndex(1, 1)))
        s.addCell(DataCell(CellIndex(1, 1), 123, "code"))
        self.assertTrue(s.hasCellAt(CellIndex(1, 1)))

    def test_getCell(self):
        s = WorksheetImp()
        cellAddr = CellIndex(12, 12)
        cell = DataCell(cellAddr, 123, "code")
        s.addCell(cell)
        self.assertEqual(cell, s.getCell(cellAddr))

    def test_isEmpty(self):
        s = WorksheetImp()
        self.assertTrue(s.isEmpty())
        cell, cellAddr = self.makeTestObj()
        s.addCell(cell)
        self.assertFalse(s.isEmpty())
        s.removeCell(cellAddr)
        self.assertTrue(s.isEmpty())

    def test_containAddress(self):
        s = WorksheetImp()
        cell, cellAddr = self.makeTestObj()
        self.assertFalse(s.containsAddress(cellAddr))
        s.addCell(cell)
        self.assertTrue(s.containsAddress(cellAddr))
        s.removeCell(cellAddr)
        self.assertFalse(s.containsAddress(cellAddr))

    def test_cells(self):
        cell1, cellAddr1 = self.makeTestObj()
        cell2, cellAddr2 = self.makeTestObj()
        s = WorksheetImp()
        s.addCell(cell1)
        s.addCell(cell2)
        self.assertEqual([cell1, cell2], s.cells)
        s.removeCell(cellAddr1)
        self.assertEqual([cell2], s.cells)

    def test_columOperation(self):
        s = WorksheetImp()
        c = ColumnImp(1, {1: DataCell(CellIndex(1, 1), 123, "code")})
        self.assertFalse(s.hasColumn(c.index))
        s.setCol(c)
        self.assertTrue(s.hasColumn(c.index))
        self.assertEqual(c, s.getCol(1))
        s.removeCol(c.index)
        self.assertTrue(s.isEmpty())

    def test_range(self):
        s = WorksheetImp()

    def test_getNonExistenceCell(self):
        s = WorksheetImp()
        c = s.getCell(CellIndex(1, 1))
        self.assertIsNotNone(c)
        self.assertTrue(s.isEmpty())
        c.code = "z"
        self.assertFalse(s.isEmpty())

        c2Addr = CellIndex(1, 2)
        c2 = s.getCell(c2Addr)
        self.assertFalse(s.hasCellAt(c2Addr))
        c2.value = 123
        self.assertTrue(s.hasCellAt(c2Addr))
