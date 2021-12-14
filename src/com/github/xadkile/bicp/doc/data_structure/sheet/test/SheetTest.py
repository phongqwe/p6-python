
import unittest

from com.github.xadkile.bicp.doc.data_structure.sheet.Sheet import SheetImp


class SheetTest(unittest.TestCase):
    def test_getNonExistenceCell(self):
        s = SheetImp.empty()
        c = s.cell(1,1)
        self.assertIsNotNone(c)
