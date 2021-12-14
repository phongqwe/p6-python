import unittest

from com.github.xadkile.bicp.doc.data_structure.cell.position.IndexCellPosition import IndexCellPosition


class IndexCellPositionTest(unittest.TestCase):
    def test_Eq(self):
        p1 = IndexCellPosition(1,2)
        p2 = IndexCellPosition(1,2)
        self.assertTrue(p1==p2)