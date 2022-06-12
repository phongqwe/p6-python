import unittest

import pandas

from com.emeraldblast.p6.document_structure.copy_paste.FullDataFrameCopier import FullDataFrameCopier
from com.emeraldblast.p6.document_structure.copy_paste.DataFramePaster import DataFramePaster
from com.emeraldblast.p6.document_structure.util.for_test.TestUtils import sampleWb


class DataFramePaster_test(unittest.TestCase):
    def test_paste(self):

        wb = sampleWb("Wb")
        rng=wb.getWorksheet(0).range("@J5:L8")

        rng.cell("@J5").value=11
        rng.cell("@K5").value="abc"
        rng.cell("@L5").value = "c"
        rng.cell("@K6").formula="=SUM(Z1:M3)"
        rng.cell("@L6").value = "'123"

        copier = FullDataFrameCopier()
        copier.copyRangeToClipboard(rng)

        paster = DataFramePaster()
        rs = paster.pasteRange()
        self.assertTrue(rs.isOk())

        rangeCopy = rs.value
        self.assertEqual(5,len(rangeCopy.cells))
        self.assertEqual(11, rangeCopy.cells[0].bareValue)
        self.assertEqual("abc", rangeCopy.cells[1].bareValue)
        self.assertEqual("c", rangeCopy.cells[2].bareValue)
        self.assertEqual("=SUM(Z1:M3)", rangeCopy.cells[3].bareFormula)
        self.assertEqual("'123", rangeCopy.cells[4].bareValue)




if __name__ == '__main__':
    unittest.main()
