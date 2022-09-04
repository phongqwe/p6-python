import unittest

from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.cell.address.CellIndex import CellIndex


class CellLabel_test(unittest.TestCase):

    def test_createAddressFromLabel(self):
        data = {
            "@A1": CellIndex(1, 1),
            "@B323": CellIndex(2, 323),
            "@ABU96": CellIndex(749, 96),
            "@GG888": CellIndex(189, 888),
            "@a1": CellIndex(1, 1),
            "@b323": CellIndex(2, 323),
            "@abu96": CellIndex(749, 96),
        }
        for k, v in data.items():
            self.assertEqual(v, CellAddresses.fromLabel(k))

    def test_constructorWithMalformedAddress(self):
        with self.assertRaises(ValueError):
            CellAddresses.fromLabel("ABU96")
        with self.assertRaises(ValueError):
            CellAddresses.fromLabel("@ABU96__")
        with self.assertRaises(ValueError):
            CellAddresses.fromLabel("@96ABU")
        with self.assertRaises(ValueError):
            CellAddresses.fromLabel("@ABU_96")
