import unittest

from com.qxdzbc.p6.cell.TestDataCell import TestDataCell

from com.qxdzbc.p6.cell.CellContent import CellContent
from com.qxdzbc.p6.cell.address.CellIndex import CellIndex
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.rpc.data_structure.CellValue import CellValue
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellProto


class DataCellTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.wbk = WorkbookKeys.fromNameAndPath("wb")
        self.wsName = "s1"


    def test_numeric_str_value(self):
        c1 = TestDataCell(address = CellIndex(1, 1), wsName = self.wsName, wbKey = self.wbk, value= "123", )
        self.assertEqual("123",c1.strValue)
        self.assertEqual("123",c1.displayValue)

        c2 = TestDataCell(address = CellIndex(1, 1), wsName = self.wsName, wbKey = self.wbk, value= "\'abc")
        self.assertEqual("\'abc", c2.strValue)
        self.assertEqual("\'abc", c2.displayValue)

    def test_sourceValue(self):
        c1 = TestDataCell(address = CellIndex(1, 1), wsName = self.wsName, wbKey = self.wbk, value=123, formula = "formula")
        self.assertEqual("formula", c1.sourceValue)

        c1 = TestDataCell(address = CellIndex(1, 1), wsName = self.wsName, wbKey = self.wbk, value=123)
        self.assertEqual(123,c1.sourceValue)

    def test_content(self):
        c1 = TestDataCell(address = CellIndex(1, 1), wsName = self.wsName, wbKey = self.wbk, value=None)
        ct1 = c1.content
        self.assertEqual(None,ct1.value)
        self.assertEqual(c1.formula, ct1.formula)

        c1 = TestDataCell(address = CellIndex(1, 1), wsName = self.wsName, wbKey = self.wbk, value=123)
        ct1 = c1.content
        self.assertEqual(c1.value, ct1.value)

    def test_content_setter(self):
        ct1 = CellContent("formula",CellValue.empty())
        c1 = TestDataCell(address = CellIndex(1, 1), wsName = self.wsName, wbKey = self.wbk, value= "v")
        c1.content = ct1
        self.assertEqual(ct1.value, c1.bareValue)
        self.assertEqual(ct1.formula, c1.bareFormula)


    def test_toProtoObj1(self):
        c1 = TestDataCell(address = CellIndex(1, 1), wsName = self.wsName, wbKey = self.wbk, value=123, formula = "formula")
        o = c1.toProtoObj()
        self.assertEqual(c1.id.toProtoObj(), o.id)
        self.assertEqual("formula", o.formula)

    def test_toProtoObj2(self):
        c1 = TestDataCell(address = CellIndex(1, 1),
                          wsName = self.wsName,
                          wbKey = self.wbk,
                          value=None)
        proto = c1.toProtoObj()
        self.assertEqual(c1.id.toProtoObj(), proto.id)
        self.assertFalse(proto.HasField("value"))
        self.assertFalse(proto.HasField("formula"))
        bt1 = c1.toProtoBytes()
        c2 = CellProto()
        c2.ParseFromString(bt1)
        print(c2)

    def test_isValueEqual(self):
        c1 = TestDataCell(address = CellIndex(1, 1), wsName = self.wsName, wbKey = self.wbk, value=123)
        c2 = TestDataCell(address = CellIndex(4, 2), wsName = self.wsName, wbKey = self.wbk, value=123)

        self.assertTrue(c1.isValueEqual(c2))
        self.assertTrue(c2.isValueEqual(c1))
        self.assertTrue(c2.isValueEqual(c2))
        c3 = TestDataCell(address = CellIndex(2, 3), wsName = self.wsName, wbKey = self.wbk, value=-234)
        self.assertFalse(c2.isValueEqual(c3))
        self.assertFalse(c3.isValueEqual(c2))

    def test_setFormula2(self):
        f = "=SUM(A1:B3)"
        c1 = TestDataCell(address = CellIndex(1, 1), wsName = self.wsName, wbKey = self.wbk, formula = f)
        c1.value=123
        c1.formula = f
        self.assertEqual(f,c1.formula)

    def test_value(self):
        c1 = TestDataCell(
            address = CellIndex(1, 1),
            wsName = self.wsName,
            wbKey = self.wbk,
            value=None
        )
        c1.value = 123
        self.assertTrue(isinstance(c1.value,int))
        print(c1.value)
