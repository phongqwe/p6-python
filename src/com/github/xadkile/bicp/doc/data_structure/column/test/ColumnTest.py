import unittest

from com.github.xadkile.bicp.doc.data_structure.cell.DataCell import DataCell
from com.github.xadkile.bicp.doc.data_structure.cell.address.CellIndex import CellIndex
from com.github.xadkile.bicp.doc.data_structure.column.ColumnImp import ColumnImp


class ColumnTest(unittest.TestCase):
    def test_queryNonExistingCell(self):
        d = {}
        r = ColumnImp(1, d)
        try:
            cell = r.getCell(CellIndex(1, 2))
            self.assertIsNotNone(cell)
            self.assertTrue(len(d)==0)
        except:
            self.fail("shouldn't raise any exception")

    def test_getNonExistingCellThenModify(self):
        r = ColumnImp.empty(2)
        pos = CellIndex(2, 1)
        cell = r.getCell(pos)
        cell.code = "abc"
        cell.value = 123
        self.assertEqual("abc", r.getCell(pos).code)
        self.assertEqual(123, r.getCell(pos).value)

    def test_isEmpty(self):
        r = ColumnImp(1, {})
        self.assertTrue(r.isEmpty())
        r.getCell(CellIndex(1, 2))
        self.assertTrue(r.isEmpty())

    def test_empty(self):
        r = ColumnImp.empty(2)
        self.assertTrue(r.isEmpty())

    def test_setCell(self):
        r = ColumnImp.empty(5)
        cell = DataCell(CellIndex(5, 1), 123, "code 1")
        r.addCell(cell)
        self.assertEqual(cell, r.getCell(CellIndex(5, 1)))

    def test_setCell_fail(self):
        with self.assertRaises(ValueError):
            r = ColumnImp.empty(5)
            cell = DataCell(CellIndex(1, 1), 123, "code 1")
            r.addCell(cell)
            self.assertEqual(cell, r.getCell(CellIndex(5, 1)))