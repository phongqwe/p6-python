import unittest

from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.address.CellAddressJson import CellAddressJson
from bicp_document_structure.workbook.WorkbookJson import WorkbookJson
from bicp_document_structure.worksheet.WorksheetJson import WorksheetJson


class WorkbookJsonTest(unittest.TestCase):
    def test_jsonCreation(self):
        wbjson = WorkbookJson([
            WorksheetJson([
                CellJson("value",None,CellAddressJson(1,2)),
                CellJson(None,"script x",CellAddressJson(1,1)),
            ]),
            WorksheetJson([
                CellJson(None, None, CellAddressJson(1, 2)),
                CellJson("value 2", "script 2", CellAddressJson(1, 1)),
            ])
        ])
        self.assertEqual("""{"worksheets": [{"cells": [{"value": "value", "script": null, "addr": [1, 2]}, {"value": null, "script": "script x", "addr": [1, 1]}]}, {"cells": [{"value": null, "script": null, "addr": [1, 2]}, {"value": "value 2", "script": "script 2", "addr": [1, 1]}]}]}""",str(wbjson))



if __name__ == '__main__':
    unittest.main()
