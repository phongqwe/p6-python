import unittest

from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.cell.address.CellIndex import CellIndex
from com.emeraldblast.p6.document_structure.range.address.RangeAddressImp import RangeAddressImp
from com.emeraldblast.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.emeraldblast.p6.document_structure.worksheet.WorksheetConst import WorksheetConst


class RangeAddressImp_test(unittest.TestCase):
    def test_fromArbitraryCells(self):
        cell1 = CellIndex(99, 88)
        cell2 = CellIndex(1, 2)
        r = RangeAddresses.fromArbitraryCells(cell1, cell2)
        expect = RangeAddressImp(cell2, cell1)
        self.assertTrue(r == expect)
        self.assertEqual(r, expect)

    def test_label(self):
        self.assertEqual("@A1:A2",RangeAddresses.addressFromLabel("@A1:A2").label)
        self.assertEqual("@A:B",RangeAddresses.addressFromLabel("@A:B").label)
        self.assertEqual("@A:B",RangeAddresses.addressFromLabel("@B:A").label)
        self.assertEqual("@20:30",RangeAddresses.addressFromLabel("@20:30").label)
        self.assertEqual("@20:30",RangeAddresses.addressFromLabel("@30:20").label)
        self.assertEqual("@A:C",
                         RangeAddresses.fromArbitraryCells(
                             CellIndex(1,1),
                             CellIndex(3,WorksheetConst.rowLimit)).label)
        self.assertEqual("@3:5",
                         RangeAddresses.fromArbitraryCells(
                             CellIndex(1, 3),
                             CellIndex(WorksheetConst.colLimit, 5)).label)

        self.assertEqual("@C:Q",
                         RangeAddresses.fromArbitraryCells(
                             CellAddresses.addressFromLabel("@C1"),
                             CellAddresses.addressFromLabel("@Q{r}".format(r=str(WorksheetConst.rowLimit)))).label)


