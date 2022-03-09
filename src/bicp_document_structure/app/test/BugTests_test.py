import unittest

from bicp_document_structure.app.GlobalScope import setIPythonGlobals
from bicp_document_structure.app.UserFunctions import *


class BugTests_test(unittest.TestCase):
    """ this class includes re-creation of actual bugs """
    def setUp(self) -> None:
        super().setUp()
        setIPythonGlobals(globals())
        startApp()
        restartApp()
        getApp().createNewWorkbook("Book1")
        getActiveWorkbook().createNewWorksheet("Sheet1")

    def test_bug1(self):
        """bug1: this wb unable to generate json"""
        app = getApp()
        w1=app.createNewWorkbook("w1")
        s1 = w1.createNewWorksheet("s1")
        c1 = s1.cell("@A1")
        c1.value=1
        c2=s1.cell("@A2")
        c2.value=2
        c3=s1.cell("@A3")
        c3.formula = """=SUM(A1:A2)"""
        c4=s1.cell("@A4")
        c4.value="abc"
        print(c1.value)
        print(c2.value)
        print(c3.value)
        print(c4.value)
        s1.toJsonStr()
