import random
import unittest

from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.column.ColumnImp import ColumnImp
from bicp_document_structure.range.RangeImp import RangeImp
from bicp_document_structure.range.address.RangeAddressImp import RangeAddressImp
from bicp_document_structure.worksheet.WorksheetImp import WorksheetImp


class WorksheetTest(unittest.TestCase):

    def test_cell(self):
        s = WorksheetImp()
        expect = DataCell(CellIndex(1, 2))

        c1 = s.cell("@A2")
        self.assertEqual(expect, c1)

        c2 = s.cell("@a2")
        self.assertEqual(expect, c2)

        c3 = s.cell((1, 2))
        self.assertEqual(expect, c3)

    def test_range(self):
        s = WorksheetImp()
        ad1 = CellIndex(1, 1)  # A1
        ad2 = CellIndex(20, 20)  # T20
        expect = RangeImp(ad1, ad2, s)

        r1 = s.range("@A1:T20")
        self.assertEqual(expect, r1)

        r2 = s.range(RangeAddressImp(ad1, ad2))
        self.assertEqual(expect, r2)

        r3 = s.range((ad1, ad2))
        self.assertEqual(expect, r3)

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
        cell = DataCell(cellAddr)
        s.addCell(cell)
        self.assertEqual(cell, s.getOrMakeCell(cellAddr))

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
        self.assertTrue(s.containsAddress(cellAddr))
        s.addCell(cell)
        self.assertTrue(s.containsAddress(cellAddr))
        s.removeCell(cellAddr)
        self.assertTrue(s.containsAddress(cellAddr))

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
        c = s.getOrMakeCell(CellIndex(1, 1))
        self.assertIsNotNone(c)
        self.assertTrue(s.isEmpty())
        c.code = "z"
        self.assertFalse(s.isEmpty())

        c2Addr = CellIndex(1, 2)
        c2 = s.getOrMakeCell(c2Addr)
        self.assertFalse(s.hasCellAt(c2Addr))
        c2.value = 123
        self.assertTrue(s.hasCellAt(c2Addr))
