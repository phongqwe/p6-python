import unittest

from com.qxdzbc.p6.document_structure.formula_translator.DirectLiteralTranslator import DirectLiteralTranslator


class DirectLiteralTranslator_test(unittest.TestCase):
    def test_something(self):
        translator = DirectLiteralTranslator()
        o1 = translator.translate("abc")
        print(o1.value)

        o2 = translator.translate("123")
        print(o2.value)
        print(type(o2.value))



if __name__ == '__main__':
    unittest.main()
