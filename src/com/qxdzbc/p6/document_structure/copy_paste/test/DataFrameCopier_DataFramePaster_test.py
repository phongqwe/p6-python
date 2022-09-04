import unittest

import pyperclip

from com.qxdzbc.p6.document_structure.app.R import R

from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.copy_paste.copier.DataFrameCopier import DataFrameCopier
from com.qxdzbc.p6.document_structure.copy_paste.paster.DataFramePaster import DataFramePaster
from com.qxdzbc.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.document_structure.util.for_test.TestUtils import sampleWb


class DataFramePaster_test(unittest.TestCase):


    def setUp(self) -> None:
        super().setUp()
        wb = sampleWb("Wb")
        rng = wb.getWorksheet(0).range("J5:L8")

        rng.cell("J5").value = 11
        rng.cell("K5").value = "abc"
        rng.cell("L5").value = "c"
        rng.cell("K6").formula = "=SUM(Z1:M3)"
        rng.cell("L6").value = "'123"
        self.wb = wb
        self.rng = rng

    def test_paste(self):

        rng = self.rng
        copier = DataFrameCopier()
        copier.copyRangeToClipboard(rng)

        paster = DataFramePaster()
        rs = paster.pasteRange(CellAddresses.fromColRow(1,1))
        self.assertTrue(rs.isOk())

        rangeCopy = rs.value
        self.assertEqual(RangeAddresses.fromLabel("A1:C4"),rangeCopy.rangeId.rangeAddress)
        self.assertEqual(5,len(rangeCopy.cells))
        self.assertEqual(11, rangeCopy.cells[0].bareValue)
        self.assertEqual("abc", rangeCopy.cells[1].bareValue)
        self.assertEqual("c", rangeCopy.cells[2].bareValue)
        self.assertEqual("=SUM(Z1:M3)", rangeCopy.cells[3].bareFormula)
        self.assertEqual("'123", rangeCopy.cells[4].bareValue)

    def test_paste_err_not_enough_space(self):

        rng = self.rng

        copier = DataFrameCopier()
        copier.copyRangeToClipboard(rng)
        paster = DataFramePaster()
        rs = paster.pasteRange(CellAddresses.fromColRow(R.WorksheetConsts.colLimit,1))
        self.assertTrue(rs.isErr())
        print(rs.err.header)

    def test_zxc(self):

        rng = self.rng

        copier = DataFrameCopier()
        copier.copyRangeToClipboard(rng)
        z = pyperclip.paste()

        print(z)









if __name__ == '__main__':
    unittest.main()
