import unittest

from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.range.address.RangeAddressImp import RangeAddressImp


class RangeAddressImp_test(unittest.TestCase):
    def test_fromArbitraryCells(self):
        cell1 = CellIndex(99, 88)
        cell2 = CellIndex(1, 2)
        r = RangeAddressImp.fromArbitraryCells(cell1, cell2)
        expect = RangeAddressImp(cell2, cell1)
        self.assertTrue(r == expect)
        self.assertEqual(r, expect)
