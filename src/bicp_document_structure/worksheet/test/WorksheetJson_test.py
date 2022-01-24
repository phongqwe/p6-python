import unittest

from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.worksheet.WorksheetJson import WorksheetJson


class WorksheetJsonTest(unittest.TestCase):
    def test_toJsonStr(self):
        cells = [
            DataCell(
                address=CellIndex(1, 1),
                value="abc",
                script=None
            ).toJson(),
            DataCell(
                address=CellIndex(1, 2),
                value=None,
                script="123"
            ).toJson()
        ]
        wjson = WorksheetJson("worksheet name",cells)
        self.assertEqual("""{"name": "worksheet name", "cells": [{"value": "abc", "script": null, "formula": null, "address": {"row": 1, "col": 1}}, {"value": null, "script": "123", "formula": null, "address": {"row": 2, "col": 1}}]}""",str(wjson))
        print(str(wjson))
    def test_fromJsonStr(self):
        jsonStr = """{"name": "worksheet name", "cells": [{"value": "abc", "script": null, "formula": null, "address": {"row": 1, "col": 1}}, {"value": null, "script": "123", "formula": null, "address": {"row": 2, "col": 1}}]}"""
        jsonObject:WorksheetJson = WorksheetJson.fromJsonStr(jsonStr)
        self.assertEqual(jsonStr,str(jsonObject))
        # todo add more test, for now this is sufficient