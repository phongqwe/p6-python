import unittest


from com.emeraldblast.p6.document_structure.copy_paste.PandasProtoCopier import PandasProtoCopier
from com.emeraldblast.p6.document_structure.copy_paste.PandasProtoPaster import PandasProtoPaster
from com.emeraldblast.p6.document_structure.util.for_test.TestUtils import sampleWb

class ProtoCopier_ProtoPaster_test(unittest.TestCase):
    def test_copy_paste(self):
        wb = sampleWb("Wb")
        rng=wb.getWorksheet(0).range("@A1:B5")
        copier = PandasProtoCopier()
        copier.copyRangeToClipboard(rng)
        #
        paster = PandasProtoPaster()
        out = paster.pasteRange()
        self.assertEqual(rng.toRangeCopy(),out)






if __name__ == '__main__':
    unittest.main()
