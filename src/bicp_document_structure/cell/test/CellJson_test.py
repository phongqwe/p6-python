import unittest

from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.address.CellAddressJson import CellAddressJson


class CellJsonTest(unittest.TestCase):
    """
    facade object design: nested
    """
    def test_toJsonStr(self):
        o = CellJson("value","script zxc","formula z",CellAddressJson(1,1))
        self.assertEqual(
            """{"value": "value", "script": "script zxc", "formula": "formula z", "address": {"row": 1, "col": 1}}""",
            str(o)
        )
    def test_fromJson(self):
        jsonStr = """{"value": "value 123", "script": "script zxc", "address": {"row": 1, "col": 1}}"""
        jsonObject = CellJson.fromJsonStr(jsonStr)
        self.assertEqual("value 123",jsonObject.value)
        self.assertEqual("script zxc",jsonObject.script)
        self.assertEqual(None,jsonObject.formula)
        self.assertEqual(CellAddressJson(1,1),jsonObject.address)

