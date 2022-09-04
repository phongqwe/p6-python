import unittest

from com.qxdzbc.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy

from com.qxdzbc.p6.document_structure.app.R import R

from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.copy_paste.copier.ProtoCopier import ProtoCopier
from com.qxdzbc.p6.document_structure.copy_paste.paster.ProtoPaster import ProtoPaster
from com.qxdzbc.p6.document_structure.util.for_test.TestUtils import sampleWb, compareList


class ProtoCopier_ProtoPaster_test(unittest.TestCase):


    def setUp(self) -> None:
        super(ProtoCopier_ProtoPaster_test, self).setUp()
        wb = sampleWb("Wb")
        rng = wb.getWorksheet(0).range("@A1:B5")
        self.rng = rng

    def test_copy_paste(self):
        rng=self.rng
        copier = ProtoCopier()
        copier.copyRangeToClipboard(rng)
        #
        paster = ProtoPaster()
        outRs = paster.pasteRange(CellAddresses.fromColRow(1,1))
        self.assertTrue(outRs.isOk())
        self.assertEqual(rng.toRangeCopy(),outRs.value)

    def test_copy_paste_error_data_too_large(self):
        rng=self.rng
        copier = ProtoCopier()
        copier.copyRangeToClipboard(rng)
        #
        paster = ProtoPaster()
        outRs = paster.pasteRange(CellAddresses.fromColRow(R.WorksheetConsts.colLimit,1))
        self.assertTrue(outRs.isErr())
        print(outRs.err.header)


if __name__ == '__main__':
    unittest.main()
