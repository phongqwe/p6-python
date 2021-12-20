import unittest

from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.column.ColumnImp import ColumnImp


class ColumnImpTest(unittest.TestCase):
    def test_empty(self):
        c = ColumnImp.empty(1)
        self.assertTrue(c.isEmpty())

    def test_index(self):
        c = ColumnImp.empty(123)
        self.assertEqual(123, c.index)

    def test_range(self):
        c = ColumnImp.empty(3)
        r = c.range(2, 10)
        self.assertIsNotNone(r)
        self.assertTrue(c.isEmpty())

    def test_queryNonExistingCell(self):
        d = {}
        r = ColumnImp(1, d)
        try:
            cell = r.getCell(CellIndex(1, 2))
            self.assertIsNotNone(cell)
            self.assertTrue(len(d) == 0)
        except:
            self.fail("shouldn't raise any exception")

    def test_getNonExistingCellThenModify_writeCellWhenSettingValue(self):
        r = ColumnImp.empty(2)
        pos = CellIndex(2, 1)
        cell = r.getCell(pos)
        cell.value = 123
        self.assertEqual(123, r.getCell(pos).value)

    def test_getNonExistingCellThenModify_writeCellWhenSettingCode(self):
        r = ColumnImp.empty(2)
        pos = CellIndex(2, 1)
        cell = r.getCell(pos)
        cell.code = "abc"
        self.assertEqual("abc", r.getCell(pos).code)

    def test_isEmpty(self):
        r = ColumnImp(1, {})
        self.assertTrue(r.isEmpty())
        r.getCell(CellIndex(1, 2))
        self.assertTrue(r.isEmpty())

    def test_addCell(self):
        r = ColumnImp.empty(5)
        cell = DataCell(CellIndex(5, 1))
        r.addCell(cell)
        self.assertEqual(cell, r.getCell(CellIndex(5, 1)))

    def test_addCell_fail(self):
        with self.assertRaises(ValueError):
            r = ColumnImp.empty(5)
            cell = DataCell(CellIndex(1, 1), 123, "code 1")
            r.addCell(cell)
            self.assertEqual(cell, r.getCell(CellIndex(5, 1)))
