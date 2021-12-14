import unittest
from collections import defaultdict

from com.github.xadkile.bicp.doc.data_structure.cell.DataCell import DataCell
from com.github.xadkile.bicp.doc.data_structure.cell.position.IndexCellPosition import IndexCellPosition


class CellBasicTest(unittest.TestCase):
    def test_Cell(self):
        c = DataCell(IndexCellPosition(1,1),123, "code 1")
        self.assertEqual(123,c.value)
        self.assertEqual("code 1",c.code)
        c.value= 345
        c.code ="code2"
        self.assertEqual(345,c.value)
        self.assertEqual("code2",c.code)

    def test_isValueEqual(self):
        c1 = DataCell(IndexCellPosition(1,1),123, "code1")
        c2 = DataCell(IndexCellPosition(4,2),123, "code2")
        c3 = DataCell(IndexCellPosition(2,3),-234, "code3")
        self.assertTrue(c1.isValueEqual(c2))
        self.assertTrue(c2.isValueEqual(c1))
        self.assertTrue(c2.isValueEqual(c2))
        self.assertFalse(c2.isValueEqual(c3))
        self.assertFalse(c3.isValueEqual(c2))
