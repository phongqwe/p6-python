import unittest

from com.github.xadkile.bicp.doc.data_structure.cell.address.CellIndexImp import CellIndex


class IndexCellPositionTest(unittest.TestCase):
    def test_Eq(self):
        p1 = CellIndex(1, 2)
        p2 = CellIndex(1, 2)
        self.assertTrue(p1==p2)