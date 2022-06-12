import unittest

import pyperclip

from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.copy_paste.paster.TextPaster import TextPaster


class TextPaster_test(unittest.TestCase):
    def test_paste(self):
        pyperclip.copy("abc")
        paster = TextPaster()
        anchorCell = CellAddresses.fromColRow(1,1)
        rs = paster.pasteRange(anchorCell = anchorCell)
        self.assertTrue(rs.isOk())
        self.assertEqual(1, len(rs.value.cells))
        self.assertEqual("abc",rs.value.cells[0].bareValue)


        pyperclip.copy("=ads")
        rs = paster.pasteRange(anchorCell = anchorCell)
        self.assertTrue(rs.isOk())
        self.assertEqual(1, len(rs.value.cells))
        self.assertEqual("=ads", rs.value.cells[0].bareFormula)


if __name__ == '__main__':
    unittest.main()
