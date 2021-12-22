import unittest

from bicp_document_structure.app.UserFunctions import startApp, getActiveWorkbook, getActiveSheet, cell


class UserFunctions_test(unittest.TestCase):
    def test_onGlobalScope(self):
        startApp()
        activeBook = getActiveWorkbook()
        activeBook.setActiveSheet("Sheet1")
        sheet = getActiveSheet()
        cellA1_1 = sheet.cell((1, 1)) #A1
        cellA1_1.code = "x=1;x+10"
        cellA1_1.runCode()
        cellA1_2 = cell("@A1")
        self.assertEqual(11,cellA1_2.value)

        cellA1_1.code = "x=2;x*50"
        self.assertEqual(11,cellA1_1._bareValue())

        cellA2 = cell("@A2")
        cellA2.setCodeAndRun("cell(\"@A1\").value+1")
        self.assertEqual(101,cellA2.value)
        self.assertEqual(100,cellA1_1.value)

        cellA3 = cell("@A3")
        cellA3.code = "cell(\"@A1\").value+ cell(\"@A2\").value"
        self.assertEqual(201,cellA3.value)

        cellA1_1.code = "cell(\"@A1\").value"
        self.assertTrue(isinstance(cellA1_1.value,Exception))
        print(cellA1_2.displayValue)

        cellA4 = cell("@A4")
        cellA4.code = "cell(\"@A3\").value + 3"
        self.assertTrue(isinstance(cellA4.value,Exception))
        print(cellA4.displayValue)




