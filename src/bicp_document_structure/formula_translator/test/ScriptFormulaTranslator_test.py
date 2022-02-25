import unittest

from bicp_document_structure.formula_translator.ScriptFormulaTranslator import ScriptFormulaTranslator


class ScriptFormulaTranslator_test(unittest.TestCase):
    def test_translate(self):
        input = {
            """    =     SCRIPT(my script)   """: """my script""",
            """=  script(my script)       """: """my script""",
            """    =sCriPT(myscript 123)""": """myscript 123""",
            """
    
    
                                                                   =SCRIPT(x=1;
f1() + f2();
while x<10:
    x= x+1
x)       
                        """ : "x=1;\n"+"f1() + f2();\n"+"while x<10:\n"+"    x= x+1\n"+"x"
        }
        translator = ScriptFormulaTranslator()
        for (i,o) in input.items():
            outRs = translator.translate(i)
            self.assertTrue(outRs.isOk())
            out = outRs.value
            self.assertEqual(o,out)

