import unittest

from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.address.CellIndex import CellIndex


class CellBasicTest(unittest.TestCase):
    def test_Cell(self):
        c = DataCell(CellIndex(1, 1), 123, "123")
        self.assertEqual(123,c.value)
        self.assertEqual("123",c.code)
        c.value= 345
        c.code ="x=345"
        self.assertEqual(345,c.value)
        self.assertEqual("x=345",c.code)

    def test_isValueEqual(self):
        c1 = DataCell(CellIndex(1, 1), 123)
        c2 = DataCell(CellIndex(4, 2), 123)

        self.assertTrue(c1.isValueEqual(c2))
        self.assertTrue(c2.isValueEqual(c1))
        self.assertTrue(c2.isValueEqual(c2))
        c3 = DataCell(CellIndex(2, 3), -234)
        self.assertFalse(c2.isValueEqual(c3))
        self.assertFalse(c3.isValueEqual(c2))

    def test_runCode(self):
        c1 = DataCell(CellIndex(1, 1), 123, "x=1;y=x*2+3;y")
        c1.runCode(globals(),None)
        self.assertEqual(5,c1.value)
