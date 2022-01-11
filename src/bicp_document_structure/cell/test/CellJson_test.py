import unittest

from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.address.CellAddressJson import CellAddressJson


class CellJsonTest(unittest.TestCase):
    def test_z(self):
        o = CellJson("value","script zxc",CellAddressJson(1,1))
        print(o)
