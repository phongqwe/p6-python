import unittest

from com.qxdzbc.p6.document_structure.cell.address.CellAddressJson import CellAddressJson
from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses


class CellAddresses_test(unittest.TestCase):
    def test_addressFromJson(self):
        json = CellAddressJson(12, 23)
        model = CellAddresses.addressFromJson(json)
        self.assertEqual(json.col, model.colIndex)
        self.assertEqual(json.row, model.rowIndex)
