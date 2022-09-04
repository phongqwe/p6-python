import unittest

from com.qxdzbc.p6.document_structure.formula_translator.WbWsFormulaTranslator import WbWsFormulaTranslator
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys


class WbWsVisitor_test(unittest.TestCase):

    def test_a(self):

        translator = WbWsFormulaTranslator("Sheet1", WorkbookKeys.fromNameAndPath("Book1","pathx"))

        inputMap = {
            "=SUM(A1:A2)": """WorksheetFunctions.SUM(getWorkbook(WorkbookKeys.fromNameAndPath("Book1","pathx")).getWorksheet("Sheet1").range("@A1:A2"))""",

            "=A1" : """getWorkbook(WorkbookKeys.fromNameAndPath("Book1","pathx")).getWorksheet("Sheet1").cell("@A1").value""",

            "=A:A":"""getWorkbook(WorkbookKeys.fromNameAndPath("Book1","pathx")).getWorksheet("Sheet1").range("@A:A")""",

            "=12:23":"""getWorkbook(WorkbookKeys.fromNameAndPath("Book1","pathx")).getWorksheet("Sheet1").range("@12:23")""",

            """=F1(F2(A2))""":"""WorksheetFunctions.F1(WorksheetFunctions.F2(getWorkbook(WorkbookKeys.fromNameAndPath("Book1","pathx")).getWorksheet("Sheet1").cell("@A2").value))""",

            """=F1(123,F2(A3,A5:B6))""":"""WorksheetFunctions.F1(123,WorksheetFunctions.F2(getWorkbook(WorkbookKeys.fromNameAndPath("Book1","pathx")).getWorksheet("Sheet1").cell("@A3").value,getWorkbook(WorkbookKeys.fromNameAndPath("Book1","pathx")).getWorksheet("Sheet1").range("@A5:B6")))"""
        }

        for (k,v) in inputMap.items():
            o = translator.translate(k)
            self.assertTrue(o.isOk())
            self.assertEqual(v,o.value)
            print(o.value)



if __name__ == '__main__':
    unittest.main()
