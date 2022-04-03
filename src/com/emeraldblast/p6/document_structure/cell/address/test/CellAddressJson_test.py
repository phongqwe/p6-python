import unittest

from com.emeraldblast.p6.document_structure.cell.address.CellAddressJson import CellAddressJson


class CellAddressJson_test(unittest.TestCase):
    def test_fromJson(self):
        jsonStr = """{"col":123,"row":234}"""
        jsonObject: CellAddressJson = CellAddressJson.fromJson(jsonStr)
        self.assertEqual(123, jsonObject.col)
        self.assertEqual(234, jsonObject.row)


if __name__ == '__main__':
    unittest.main()
