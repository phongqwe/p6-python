
import unittest

from com.github.xadkile.bicp.doc.data_structure.sheet.Sheet import Sheet


class SheetTest(unittest.TestCase):
    def test_getNonExistenceCell(self):
        s = Sheet.empty()
        c = s.cell(1,1)
        self.assertIsNotNone(c)
