import unittest

from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.cell.address.CellLabel import CellLabel


class CellLabel_test(unittest.TestCase):

    def test_constructor(self):
        data = {
            "A1": CellIndex(1, 1),
            "B323": CellIndex(2, 323),
            "ABU96": CellIndex(749, 96),
            "GG888": CellIndex(189, 888)
        }
        for k,v in data.items():
            self.assertEqual(v, CellLabel(k))

