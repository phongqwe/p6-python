import unittest

from com.qxdzbc.p6.document_structure.app.GlobalScope import setIPythonGlobals
from com.qxdzbc.p6.document_structure.app.TopLevel import *


class UserFunctions_test(unittest.TestCase):
    """
    these tests emulate code execution from the front end
    """
    pass
    # def setUp(self) -> None:
    #     super().setUp()
    #     setIPythonGlobals(globals())
    #     startApp()
    #     restartApp()
    #     getApp().createNewWorkbook("Book1")
    #     getActiveWorkbookRs().createNewWorksheet("Sheet1")
    #
    # def test_codeExecution_directLiteral(self):
    #     cell("A1").script = "100"
    #     self.assertEqual(100, cell("A1").value)
    #
    # def test_codeExecution_functionCall(self):
    #     cell("A1").script = "len([1,2,3])"
    #     self.assertEqual(3, cell("A1").value)
    #
    # def test_listWorkSheet(self):
    #     print(listWorksheet("Book1"))
    #     print(listWorksheet())
    #     print(printWorkbookSummary())
