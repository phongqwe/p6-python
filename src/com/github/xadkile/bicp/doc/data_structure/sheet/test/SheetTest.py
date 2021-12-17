
import unittest

from com.github.xadkile.bicp.doc.data_structure.cell.DataCell import DataCell
from com.github.xadkile.bicp.doc.data_structure.cell.address.CellIndex import CellIndex
from com.github.xadkile.bicp.doc.data_structure.sheet.Worksheet import Worksheet


class SheetTest(unittest.TestCase):
    def test_hasCellAt(self):
        s = Worksheet()
        self.assertFalse(s.hasCellAt(CellIndex(1,1)))
        s.addCell(DataCell(CellIndex(1,1),123,"code"))
        self.assertTrue(s.hasCellAt(CellIndex(1,1)))

    def test_getCell(self):
        s = Worksheet()
        cellAddr = CellIndex(12, 12)
        cell = DataCell(cellAddr, 123, "code")
        s.addCell(cell)
        self.assertEqual(cell,s.getCell(cellAddr))


    def test_getNonExistenceCell(self):
        s = Worksheet()
        c = s.getCell(CellIndex(1,1))
        self.assertIsNotNone(c)
        self.assertTrue(s.isEmpty())
        c.code="z"
        self.assertFalse(s.isEmpty())

        c2Addr = CellIndex(1,2)
        c2 = s.getCell(c2Addr)
        self.assertFalse(s.hasCellAt(c2Addr))
        c2.value = 123
        self.assertTrue(s.hasCellAt(c2Addr))

