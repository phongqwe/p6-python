import unittest

from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.address.CellIndex import CellIndex


class CellIndexTest(unittest.TestCase):

    def test_Eq(self):
        class DummyAddress(CellAddress):
            def __init__(self,c,r):
                self.r = r
                self.c = c
            @property
            def rowIndex(self) -> int:
                return self.r

            @property
            def colIndex(self) -> int:
                return self.c

        p1 = CellIndex(1, 2)
        p2 = CellIndex(1, 2)
        p3 = DummyAddress(1,2)
        self.assertTrue(p1 == p2)
        self.assertFalse(p1 == "abc")
        self.assertTrue(p1 == p3)
        self.assertFalse(CellIndex(100,200) == p3)

    def test_label(self):
        lb = CellIndex(2, 323).label
        self.assertEqual("@B323",lb)
