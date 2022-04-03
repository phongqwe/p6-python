import unittest

from com.emeraldblast.p6.document_structure.formula_translator.PythonLangElements import PythonLangElements
from com.emeraldblast.p6.document_structure.formula_translator.StdFormulaTranslator import StdFormulaTranslator


class FormulaTranslatorFinal_test(unittest.TestCase):

    def test_translate(self):
        f = PythonLangElements.worksheetFunctions
        literalInput = {
            "=123": "123",
            "=123.123": "123.123",
            "=-123": "-123",
            "=+123": "+123",
            "=0-123": "0-123",
            "=2^3^4": "2**3**4",
            "=1+2": "1+2",
            "=1+2.3+4": "1+2.3+4",
            "=(-12+33)*9-(((222)))": "(-12+33)*9-(((222)))",
            "=\"\"": "\"\"",
            "=\"abc\"": "\"abc\"",
            "=\"123\"": "\"123\"",
            "=\"abc\"+1": "\"abc\"+1",
            "=\"abc\"+1+\"x\"": "\"abc\"+1+\"x\"",
            "=123+\"qwe\"": "123+\"qwe\"",
            "=2^(2+3-1)*9": "2**(2+3-1)*9",
            "=2^(-1)": "2**(-1)",
        }

        directLiteral = {
            "123": "123",
            "123abc": "\"\"\"123abc\"\"\"",
            "\"abc\"": "\"\"\"abc\"\"\"",
            "abc": "\"\"\"abc\"\"\"",
            "\"abc": "\"\"\"\"abc\"\"\"",
            "     abc": "\"\"\"     abc\"\"\"",
            "abc\nccc\n\t": "\"\"\"abc\nccc\n\t\"\"\"",
        }
        functionLiteralInput = {
            "=sum()": "{f}.sum()".format(f=f),
            """=sum(1,2,3.3)""": """{f}.sum(1,2,3.3)""".format(f=f),
            """=sum(1,2,3.3,"abc")""": """{f}.sum(1,2,3.3,"abc")""".format(f=f),
            """=f1(1,2,3.3,"qwe",f2())""": """{f}.f1(1,2,3.3,"qwe",{f}.f2())""".format(f=f),
            """=f1(1,2,3.3,"qwe",f2(1,"ab"))""": """{f}.f1(1,2,3.3,"qwe",{f}.f2(1,"ab"))""".format(f=f),
            """=mf(1+2,"b",-1)""": """{f}.mf(1+2,"b",-1)""".format(f=f),
        }
        range = {
            "=f(A1)": """{f}.f(cell("@A1").value)""".format(f=f),
            "=f(AB1123)": """{f}.f(cell("@AB1123").value)""".format(f=f),
            "=f(A1:C4)": """{f}.f(getRange("@A1:C4"))""".format(f=f),
            "=f(AK11:CX34)": """{f}.f(getRange("@AK11:CX34"))""".format(f=f),
            "=f(1:123)": """{f}.f(getRange("@1:123"))""".format(f=f),
            "=f(A:b)": """{f}.f(getRange("@A:b"))""".format(f=f),
            "=f(sheet1!A:b)": """{f}.f(getWorksheet("sheet1").getRange("@A:b"))""".format(f=f),
            "=f(sheet1!A123)": """{f}.f(getWorksheet("sheet1").cell("@A123").value)""".format(f=f),
            "=f('my sheet1'!A123)": """{f}.f(getWorksheet("my sheet1").cell("@A123").value)""".format(f=f),
            "=f('sheet1 23'!A123)": """{f}.f(getWorksheet("sheet1 23").cell("@A123").value)""".format(f=f),
        }
        composite = {
            """=f1(1,A1,B34:z9, "zzz",-234,1+2*3,C1)""": """{f}.f1(1,cell("@A1").value,getRange("@B34:z9"),"zzz",-234,1+2*3,cell("@C1").value)""".format(f=f),
            """=f1(f2(),f3(f4(),f5()))""": """{f}.f1({f}.f2(),{f}.f3({f}.f4(),{f}.f5()))""".format(f=f),
            """=f1(f2(1,2^7*9,"A1"),f3(f4(1+f9()),f5("az"+f9())))""": """{f}.f1({f}.f2(1,2**7*9,"A1"),{f}.f3({f}.f4(1+{f}.f9()),{f}.f5("az"+{f}.f9())))""".format(
                f=f),
        }
        script = {
            """    =     SCRIPT(my script)   """: """my script""",
            """=  script(my script)       """: """my script""",
            """    =sCriPT(myscript 123)""": """myscript 123""",
            """
    
    
                                                                   =SCRIPT(x=1;
f1() + f2();
while x<10:
    x= x+1
x)       
                        """: "x=1;\n" + "f1() + f2();\n" + "while x<10:\n" + "    x= x+1\n" + "x"
        }

        all = {}
        all.update(literalInput)
        all.update(functionLiteralInput)
        all.update(range)
        all.update(composite)
        all.update(script)
        all.update(directLiteral)

        translator = StdFormulaTranslator()
        for (i,o) in all.items():
            outRs = translator.translate(i)
            self.assertTrue(outRs.isOk())
            self.assertEqual(o, outRs.value)
