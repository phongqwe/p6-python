import unittest

from bicp_document_structure.app.run_result.RunResultJson import RunResultJson
from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.address.CellAddressJson import CellAddressJson


class RunResultJsonTest(unittest.TestCase):
    def test_create(self):
        o = RunResultJson(
            [CellJson("value1","script 1", CellAddressJson(1,2))],
            [CellJson("value2","script 2", CellAddressJson(2,2))],
        )
        print(o)