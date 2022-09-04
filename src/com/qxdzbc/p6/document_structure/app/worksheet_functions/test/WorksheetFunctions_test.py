import unittest

from com.qxdzbc.p6.document_structure.app.GlobalScope import setIPythonGlobals
from com.qxdzbc.p6.document_structure.app.TopLevel import getRange, startApp, getApp, getActiveWorkbookRs
from com.qxdzbc.p6.document_structure.app.worksheet_functions.WorksheetFunctions import WorksheetFunctions


class WorksheetFunctions_test(unittest.TestCase):
    def test_something(self):
        setIPythonGlobals(globals())
        startApp()
        getApp().createNewWorkbook()
        getActiveWorkbookRs().createNewWorksheet("Sheet1")
        r = getRange("A1:A2")
        r.cell("A1").value=100
        o = WorksheetFunctions.SUM(getRange("A1:A2"))
        self.assertEqual(100, o)
