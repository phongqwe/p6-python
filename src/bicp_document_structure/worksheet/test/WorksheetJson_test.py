import unittest

from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.worksheet.WorksheetJson import WorksheetJson


class WorksheetJsonTest(unittest.TestCase):
    def test_zz(self):
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
        self.assertEqual("""{"name": "worksheet name", "cells": [{"value": "abc", "script": null, "addr": [1, 1]}, {"value": null, "script": "123", "addr": [1, 2]}]}""",str(wjson))


