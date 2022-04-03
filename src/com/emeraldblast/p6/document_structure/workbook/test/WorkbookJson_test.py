import unittest

from com.emeraldblast.p6.document_structure.cell.CellJson import CellJson
from com.emeraldblast.p6.document_structure.cell.address.CellAddressJson import CellAddressJson
from com.emeraldblast.p6.document_structure.workbook.WorkbookJson import WorkbookJson
from com.emeraldblast.p6.document_structure.worksheet.WorksheetJson import WorksheetJson


class WorkbookJsonTest(unittest.TestCase):
    def test_jsonCreation(self):
        wbjson = WorkbookJson("workbookName",None,[
            WorksheetJson("sheet1",[
                CellJson("value",None,None,CellAddressJson(1,2)),
                CellJson(None,"script x",None,CellAddressJson(1,1)),
            ]),
            WorksheetJson("sheet2",[
                CellJson(None, None,None ,CellAddressJson(1, 2)),
                CellJson("value 2", "script 2", None,CellAddressJson(1, 1)),
            ])
        ])
        self.assertEqual("""{"name": "workbookName", "path": null, "worksheets": [{"name": "sheet1", "cells": [{"value": "value", "script": null, "formula": null, "address": {"row": 2, "col": 1}}, {"value": null, "script": "script x", "formula": null, "address": {"row": 1, "col": 1}}]}, {"name": "sheet2", "cells": [{"value": null, "script": null, "formula": null, "address": {"row": 2, "col": 1}}, {"value": "value 2", "script": "script 2", "formula": null, "address": {"row": 1, "col": 1}}]}]}""",str(wbjson))
    def test_fromJsonStr(self):
        jsonStr = """{"name": "qwe", "path": null, "worksheets": [{"name": "sheet1", "cells": [{"value": "value", "script": null, "formula": null, "address": {"row": 2, "col": 1}}, {"value": null, "script": "script x", "formula": null, "address": {"row": 1, "col": 1}}]}, {"name": "sheet2", "cells": [{"value": null, "script": null, "formula": null, "address": {"row": 2, "col": 1}}, {"value": "value 2", "script": "script 2", "formula": null, "address": {"row": 1, "col": 1}}]}]}"""
        o = WorkbookJson.fromJsonStr(jsonStr)
        self.assertEqual(jsonStr,str(o))
        # todo add more test, for now this is kinda sufficient

if __name__ == '__main__':
    unittest.main()
