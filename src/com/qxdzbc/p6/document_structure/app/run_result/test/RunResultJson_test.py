import unittest

from com.qxdzbc.p6.document_structure.cell.CellJson import CellJson

from com.qxdzbc.p6.document_structure.app.run_result.RunResultJson import RunResultJson
from com.qxdzbc.p6.document_structure.cell.address.CellAddressJson import CellAddressJson


class RunResultJsonTest(unittest.TestCase):
    def test_create(self):
        o = RunResultJson(
            [CellJson("value1", "script 1", None, CellAddressJson(1, 2))],
            [CellJson("value2", "script 2", None, CellAddressJson(2, 2))],
        )
        print(o)
