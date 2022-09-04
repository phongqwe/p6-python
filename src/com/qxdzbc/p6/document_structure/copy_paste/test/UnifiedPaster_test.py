import unittest
from unittest.mock import MagicMock

import pyperclip

from com.qxdzbc.p6.document_structure.app.R import R

from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.copy_paste.copier.DataFrameCopier import DataFrameCopier
from com.qxdzbc.p6.document_structure.copy_paste.copier.ProtoCopier import ProtoCopier
from com.qxdzbc.p6.document_structure.copy_paste.paster.DataFramePaster import DataFramePaster
from com.qxdzbc.p6.document_structure.copy_paste.paster.Pasters import Pasters
from com.qxdzbc.p6.document_structure.copy_paste.paster.ProtoPaster import ProtoPaster
from com.qxdzbc.p6.document_structure.copy_paste.paster.UnifiedPaster import UnifiedPaster
from com.qxdzbc.p6.document_structure.util.Util import compareList
from com.qxdzbc.p6.document_structure.util.for_test.TestUtils import sampleWb
from com.qxdzbc.p6.document_structure.util.result.Err import Err
from com.qxdzbc.p6.document_structure.util.result.Ok import Ok


class UnifiedPaster_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        wb = sampleWb("Wb")
        rng = wb.getWorksheet(0).range("@A1:B5")
        self.rng = rng
        self.protoPaster = MagicMock()
        self.textPaster = MagicMock()
        self.dfPaster = MagicMock()

        self.protoPaster.pasteRange = MagicMock(return_value = Ok("protoPaster"))
        self.textPaster.pasteRange = MagicMock(return_value = Ok("textPaster"))
        self.dfPaster.pasteRange = MagicMock(return_value = Ok("dfPaster"))

        self.paster = UnifiedPaster(
            protoPaster = self.protoPaster,
            textPaster = self.textPaster,
            dfPaster = self.dfPaster,
        )

    def test_copy_paste_proto(self):
        rng=self.rng
        copier = ProtoCopier()
        copier.copyRangeToClipboard(rng)
        outRs = self.paster.pasteRange(CellAddresses.fromColRow(1,1))

        self.protoPaster.pasteRange.assert_called_once()
        self.textPaster.pasteRange.assert_not_called()
        self.dfPaster.pasteRange.assert_not_called()

        self.assertTrue(outRs.isOk())
        self.assertEqual("protoPaster", outRs.value)

    def test_paste_dataframe(self):
        rng=self.rng
        copier = DataFrameCopier()
        copier.copyRangeToClipboard(rng)
        
        self.protoPaster.pasteRange=MagicMock(return_value=Err(None))

        outRs = self.paster.pasteRange(CellAddresses.fromColRow(1, 1))
        self.assertTrue(outRs.isOk())
        self.protoPaster.pasteRange.assert_called_once()
        self.textPaster.pasteRange.assert_not_called()
        self.dfPaster.pasteRange.assert_called_once()

        outRs = self.paster.pasteRange(CellAddresses.fromColRow(1,1))
        self.assertTrue(outRs.isOk())
        self.assertEqual("dfPaster", outRs.value)


    def test_paste_text(self):
        pyperclip.copy("asd")
        self.protoPaster.pasteRange = MagicMock(return_value = Err(None))
        self.dfPaster.pasteRange = MagicMock(return_value = Err(None))
        outRs = self.paster.pasteRange(CellAddresses.fromColRow(1, 1))
        self.assertTrue(outRs.isOk())
        self.assertEqual("textPaster", outRs.value)

    def test_1(self):
        rng = self.rng
        copier = ProtoCopier()
        copier.copyRangeToClipboard(rng)
        outRs = Pasters.unifiedPaster.pasteRange(CellAddresses.fromColRow(23,32))
        self.assertEqual(rng.toRangeCopy(),outRs.value)

    def test_2(self):
        rng = self.rng
        copier = DataFrameCopier()
        copier.copyRangeToClipboard(rng)
        outRs = Pasters.unifiedPaster.pasteRange(CellAddresses.fromColRow(23,32))
        # range ids are not equal because the paster construct a fake rangeId for its RangeCopy
        self.assertEqual(rng.toRangeCopy().rangeId.rangeAddress,outRs.value.rangeId.rangeAddress)
        self.assertTrue(compareList(rng.toRangeCopy().cells,outRs.value.cells))

    def test_3(self):
        rng = self.rng
        text="qwe"
        pyperclip.copy(text)
        outRs = Pasters.unifiedPaster.pasteRange(CellAddresses.fromColRow(23, 32))
        self.assertTrue(outRs.isOk())
        self.assertEqual(1,len(outRs.value.cells))
        self.assertEqual(text,(outRs.value.cells[0].bareValue))

    def test_4(self):
        outRs = Pasters.unifiedPaster.pasteRange(CellAddresses.fromColRow(23, 32))
        self.assertTrue(outRs.isOk())





if __name__ == '__main__':
    unittest.main()
