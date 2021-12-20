import unittest

from bicp_document_structure.app.UserFunctions import startApp, getActiveWorkbook, getActiveSheet, getCell


class UserFunctions_test(unittest.TestCase):
    def test_onGlobalScope(self):
        startApp()
        activeBook = getActiveWorkbook()
        activeBook.createNewSheet("Sheet1")
        activeBook.setActiveSheet("Sheet1")
        sheet = getActiveSheet()
        cell1 = sheet.cell((1, 1)) #A1
        cell1.code = "x=1;x+10"
        cell1.runCode()
        cell2 = getCell("A1")
        self.assertEqual(11,cell2.value)
