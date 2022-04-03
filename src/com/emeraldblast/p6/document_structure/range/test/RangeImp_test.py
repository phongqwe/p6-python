import unittest
from unittest.mock import MagicMock

from com.emeraldblast.p6.document_structure.cell.address.CellIndex import CellIndex
from com.emeraldblast.p6.document_structure.range.RangeImp import RangeImp


class RangeImpTest(unittest.TestCase):

    def makeTestObj(self):
        parent = MagicMock()
        firstCell = CellIndex(1, 1)
        lastCell = CellIndex(3, 9)
        r = RangeImp(firstCell, lastCell, parent)
        return r, parent



    def test_constructor(self):
        parent = MagicMock()
        firstCell = CellIndex(1, 1)
        lastCell = CellIndex(3, 9)
        parent.containsAddress(firstCell, lastCell).return_value = True
        # parent.containsAddress.return_value = True
        try:
            RangeImp(firstCell, lastCell, parent)
        except:
            self.fail("should not throw exception")

        failAddress = CellIndex(-1, -1)
        parent.containsAddress(firstCell, failAddress).return_value = False
        #
        # parent.containsAddress.return_value = False

        with self.assertRaises(ValueError):
            RangeImp(firstCell, failAddress, parent)

    def test_3method(self):
        r, parent = self.makeTestObj()
        # containsAddress
        self.assertTrue(r.containsAddress(CellIndex(2, 2)))
        self.assertFalse(r.containsAddress(CellIndex(0, 0)))
        self.assertFalse(r.containsAddress(CellIndex(10, 100)))
        # firstCellAddress & lastCellAddress
        self.assertEqual(CellIndex(1, 1), r.firstCellAddress)
        self.assertEqual(CellIndex(3, 9), r.lastCellAddress)

    def test_hasCell(self):
        r, parent = self.makeTestObj()
        c = CellIndex(2, 2)

        def sideEffect(a): return a != c

        parent.hasCellAt.side_effect = sideEffect
        self.assertFalse(r.hasCellAt(c))

        def sideEffect2(a): return a == c

        parent.hasCellAt.side_effect = sideEffect2
        self.assertTrue(r.hasCellAt(c))

        c2 = CellIndex(100, 100)
        self.assertFalse(r.hasCellAt(c2))

    def test_getOrMakeCell(self):
        r, parent = self.makeTestObj()
        ad1 = CellIndex(2, 2)

        # get cell exists in parent container
        def se(a):
            if a == ad1:
                return 123
            else:
                return None

        parent.getCell.side_effect = se
        self.assertIsNotNone(r.getOrMakeCell(ad1))

        # get cell NOT exist in parent container
        def se2(a):
            if a == ad1:
                raise LookupError
            else:
                return 123

        parent.getCell.side_effect = se2
        # with self.assertRaises(LookupError):
        #     r.getOrMakeCell(ad1)

        # get cell out of range
        with self.assertRaises(ValueError):
            r.getOrMakeCell(CellIndex(100, 100))

    def test_cells(self):
        r,parent = self.makeTestObj()
        self.assertTrue(len(r.cells)==0)