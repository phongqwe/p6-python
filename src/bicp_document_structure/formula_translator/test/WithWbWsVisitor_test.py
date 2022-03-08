import unittest

from bicp_document_structure.formula_translator.PythonFormulaTranslator import PythonFormulaTranslator
from bicp_document_structure.formula_translator.PythonFormulaVisitor import PythonFormulaVisitor
from bicp_document_structure.formula_translator.WithWbWsVisitor import WithWbWsVisitor
from bicp_document_structure.workbook.WorkbookKeys import WorkbookKeys


class WithWbWsVisitor_test(unittest.TestCase):

    def test_a(self):
        translator = PythonFormulaTranslator(
            visitor = WithWbWsVisitor(
                sheetName = "Sheet1",
                workbookKey = WorkbookKeys.fromNameAndPath("Book1","pathx"),
                visitor=PythonFormulaVisitor()
            )
        )

        inputMap = {
            "=SUM(A1:A2)": """WorksheetFunctions.SUM(getWorkbook(WorkbookKeys.fromNameAndPath("Book1","pathx")).getSheet("Sheet1").getRange("@A1:A2"))""",

            "=A1" : """getWorkbook(WorkbookKeys.fromNameAndPath("Book1","pathx")).getSheet("Sheet1").cell("@A1").value""",

            "=A:A":"""getWorkbook(WorkbookKeys.fromNameAndPath("Book1","pathx")).getSheet("Sheet1").getRange("@A:A")""",

            "=12:23":"""getWorkbook(WorkbookKeys.fromNameAndPath("Book1","pathx")).getSheet("Sheet1").getRange("@12:23")""",

            """=F1(F2(A2))""":"""WorksheetFunctions.F1(WorksheetFunctions.F2(getWorkbook(WorkbookKeys.fromNameAndPath("Book1","pathx")).getSheet("Sheet1").cell("@A2").value))""",

            """=F1(123,F2(A3,A5:B6))""":"""WorksheetFunctions.F1(123,WorksheetFunctions.F2(getWorkbook(WorkbookKeys.fromNameAndPath("Book1","pathx")).getSheet("Sheet1").cell("@A3").value,getWorkbook(WorkbookKeys.fromNameAndPath("Book1","pathx")).getSheet("Sheet1").getRange("@A5:B6")))"""
        }

        for (k,v) in inputMap.items():
            o = translator.translate(k)
            self.assertTrue(o.isOk())
            self.assertEqual(v,o.value)
            print(o.value)



if __name__ == '__main__':
    unittest.main()
