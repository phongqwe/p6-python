import unittest

from com.emeraldblast.p6.document_structure.formula_translator.PythonFormulaTranslator import PythonFormulaTranslator
from com.emeraldblast.p6.document_structure.formula_translator.PythonFormulaVisitor import PythonFormulaVisitor


class PythonFormulaTranslator_test(unittest.TestCase):
    def test_translate_fail(self):
        script = [
            "a",
            "abc",
            "=f(123",
            """=f(1,"a")2+3""",
            """1+1+2""",
            "\"a\"",
            "123",
            "---",
            "@#$123",
            "=23!",
            """=f1(f2(1,2^7*9,"A1"),f3(f4(1+f9(),f5("az"+f9())))""",
            "f(sheet1!A123)",
            "f(sheet1!A123)",
            "=f(sheet1 23!A123)",
            """=sum(1,2,3.3,abc)""",
            """=sum(1,2,3.3,abc")""",
            """=sum(1,2,3.3,"abc)""",
        ]
        translator = PythonFormulaTranslator(visitor = PythonFormulaVisitor())
        for i in script:
            outRs = translator.translate(i)
            self.assertTrue(outRs.isErr(),i)