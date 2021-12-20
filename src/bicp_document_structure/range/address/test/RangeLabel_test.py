import unittest

from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.range.address.RangeAddressImp import RangeAddressImp
from bicp_document_structure.range.address.RangeLabel import RangeLabel


class RangeLabel_test(unittest.TestCase):
    def test_constructor(self):
        data = {
            "A1:A2":RangeAddressImp(CellIndex(1,1),CellIndex(1,2)),
            "m32:Ab200":RangeAddressImp(CellIndex(13,32),CellIndex(28,200)),
            "m32:ab200":RangeAddressImp(CellIndex(13,32),CellIndex(28,200)),
            "m32:AB200":RangeAddressImp(CellIndex(13,32),CellIndex(28,200)),
            "M32:ab200":RangeAddressImp(CellIndex(13,32),CellIndex(28,200)),
        }

        for k,v in data.items():
            label = RangeLabel(k)
            self.assertEqual(label,v)
