import unittest
from collections import defaultdict

from com.github.xadkile.bicp.doc.data_structure.cell.DataCell import DataCell
from com.github.xadkile.bicp.doc.data_structure.cell.position.IndexCellPosition import IndexCellPosition
from com.github.xadkile.bicp.doc.data_structure.column.Column import Column


class ColumnTest(unittest.TestCase):
    def test_queryNonExistingCell(self):
        d = {}
        r = Column(1,d)
        try:
            cell = r.getCell(IndexCellPosition.forCol(1))
            self.assertIsNotNone(cell)
            self.assertTrue(len(d)==0)
        except:
            self.fail("shouldn't raise any exception")

    def test_addingCell(self):
        r = Column.empty(2)
        cell = r.getCell(1)
        cell.code = "abc"
        cell.value = 123
        self.assertEqual("abc", r.getCell(1).code)
        self.assertEqual(123, r.getCell(1).value)

    def test_getCellWithIncorrectTypeKey(self):
        r = Column.empty(3)
        with self.assertRaises(ValueError):
            r.getCell("key")

    def test_isEmpty(self):
        r = Column(1,{})
        self.assertTrue(r.isEmpty())
        r.getCell(IndexCellPosition.forCol(2))
        self.assertTrue(r.isEmpty())

    def test_empty(self):
        r = Column.empty(2)
        self.assertTrue(r.isEmpty())

    def test_addCell(self):
        r = Column.empty(5)
        cell = DataCell(IndexCellPosition(5,1),123,"code 1")
        r.addCell(1,cell)
        self.assertEqual(cell, r.getCell(1))

