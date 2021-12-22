import unittest

from bicp_document_structure.app.UserFunctions import getRange, restartApp
from bicp_document_structure.app.worksheet_functions.WorksheetFunctions import WorksheetFunctions


class WorksheetFunctions_test(unittest.TestCase):
    def test_something(self):
        restartApp()
        r = getRange("@A1:A2")
        r.cell("@A1").value=100
        o = WorksheetFunctions.sum(r)
        self.assertEqual(100, o)
