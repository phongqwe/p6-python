import unittest

from com.qxdzbc.p6.document_structure.cell.DataCell import DataCell
from com.qxdzbc.p6.document_structure.cell.EventCell import EventCell
from com.qxdzbc.p6.document_structure.workbook.WorkbookImp import WorkbookImp

from com.qxdzbc.p6.document_structure.cell.CellContent import CellContent
from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.cell.address.CellIndex import CellIndex
from com.qxdzbc.p6.new_architecture.rpc.data_structure.CellValue import CellValue
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellProto


class DataCellTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.wb = WorkbookImp("wb")
        self.s = self.wb.createNewWorksheet("s1")

    def test_numeric_str_value(self):
        c1 = DataCell(CellIndex(1, 1), "\'123")
        self.assertEqual("123",c1.strValue)
        self.assertEqual("123",c1.displayValue)

        c2 = DataCell(CellIndex(1, 1), "\'abc")
        self.assertEqual("\'abc", c2.strValue)
        self.assertEqual("\'abc", c2.displayValue)

    def test_sourceValue(self):
        c1 = DataCell(CellIndex(1, 1), 123, "formula", "script")
        self.assertEqual("formula", c1.sourceValue)

        c1 = DataCell(CellIndex(1, 1), 123, None, None)
        self.assertEqual(123,c1.sourceValue)

    def test_content(self):
        c1 = DataCell(CellIndex(1, 1), 123, "formula", "script")
        ct1 = c1.content
        self.assertEqual(None,ct1.value)
        self.assertEqual(c1.formula, ct1.formula)
        self.assertEqual(c1.script, ct1.script)

        c1 = DataCell(CellIndex(1, 1), 123, None, None)
        ct1 = c1.content
        self.assertEqual(c1.value, ct1.value)

    def test_content_setter(self):
        ct1 = CellContent("formula",CellValue.empty())
        c1 = DataCell(CellIndex(1,2),"z","q","x")
        c1.content = ct1
        self.assertEqual(ct1.value, c1.bareValue)
        self.assertEqual(ct1.formula, c1.bareFormula)


    def test_toProtoObj1(self):
        c1 = DataCell(CellIndex(1, 1), 123, "formula", "script")
        o = c1.toProtoObj()
        self.assertEqual(c1.address.toProtoObj(), o.address)
        self.assertEqual("formula", o.formula)

    def test_toProtoObj2(self):

        c1 = DataCell(CellIndex(1, 1))
        proto = c1.toProtoObj()
        self.assertEqual(c1.address.toProtoObj(), proto.address)
        self.assertFalse(proto.HasField("value"))
        self.assertFalse(proto.HasField("formula"))
        bt1 = c1.toProtoBytes()
        c2 = CellProto()
        c2.ParseFromString(bt1)
        print(c2)


    def test_clearScriptResult(self):
        c1 = DataCell(CellIndex(1, 1), 123)
        c1.clearScriptResult()
        self.assertEqual(123, c1.bareValue)

        c2 = DataCell(CellIndex(1, 1), 123, script = "123")
        c2.clearScriptResult()
        self.assertIsNone(c2.bareValue)
        self.assertIsNotNone(c2.script)

        c3 = DataCell(CellIndex(1, 1))
        c3.clearScriptResult()
        self.assertIsNone(c3.bareValue)
        self.assertIsNone(c3.script)

    def test_rerun(self):
        self.exCountA = 0

        def increaseExCount(eventData):
            self.exCountA += 1

        wb = WorkbookImp("B1")
        s1 = wb.createNewWorksheet("S1")
        c1 = s1.cell((1,1))
        c1.value=123
        c1.script="123"
        c2 = EventCell(c1,
                       onCellEvent = increaseExCount)
        oldCount = self.exCountA
        c2.reRun(globals())
        self.assertEqual(123, c2.bareValue)
        # +1 when clear, and +1 when run
        self.assertEqual(oldCount + 1, self.exCountA)
        oldCount = self.exCountA
        c2.reRun(globals())
        self.assertEqual(123, c2.bareValue)
        self.assertEqual(oldCount + 1, self.exCountA)

    def test_assigningValueAndScript(self):
        c = DataCell(CellIndex(1, 1))
        self.assertIsNone(c.value)
        self.assertIsNone(c.script)
        c.value = 123
        self.assertEqual(123, c.value)
        self.assertIsNone(c.script)

        # x: result 11 from running script should overwrite the old value 123
        c.script = "x=10;x=x+1;x;"
        self.assertIsNone(c.bareValue)
        c.runScript(globals())
        self.assertTrue(c.isValueEqual(11))
        self.assertEqual(11, c.value)

    def test_caching(self):
        self.exCount = 0

        def increaseExCount(data):
            self.exCount += 1

        wb = WorkbookImp("B1")
        s1 = wb.createNewWorksheet("S1")
        c1 = s1.cell((1, 1))

        c = EventCell(c1, onCellEvent = increaseExCount)
        c.script = "x=345;\"abc\""
        oldCount = self.exCount
        c.reRun(globals())
        self.assertEqual("abc", c.value)
        self.assertEqual(oldCount + 1, self.exCount)

        # access value a second time
        # cell mutation callback should not be invoked this time
        # because the run result was cache, the script should not run this time
        self.assertEqual(oldCount + 1, self.exCount)

    def test_setScript(self):
        c = self.s.cell((1,1))
        c.value = 123
        self.assertEqual(123, c.value)
        self.assertEqual(None, c.script)
        c.value = 345
        # x: set valid script
        c.script = "x=345;\"abc\""
        c.runScript()
        self.assertEqual("abc", c.bareValue)
        self.assertEqual("x=345;\"abc\"", c.script)

        # x: set empty script
        c.script = ""
        self.assertEqual(None, c.value)

    def test_isValueEqual(self):
        c1 = DataCell(CellIndex(1, 1), 123)
        c2 = DataCell(CellIndex(4, 2), 123)

        self.assertTrue(c1.isValueEqual(c2))
        self.assertTrue(c2.isValueEqual(c1))
        self.assertTrue(c2.isValueEqual(c2))
        c3 = DataCell(CellIndex(2, 3), value = -234)
        self.assertFalse(c2.isValueEqual(c3))
        self.assertFalse(c3.isValueEqual(c2))

    def test_runCode(self):
        c1 = DataCell(CellIndex(1, 1), 123, script = "x=1;y=x*2+3;y")
        c1.runScript()
        self.assertEqual(5, c1.value)

    def test_setFormula1(self):
        c1 = self.s.cell((1, 1))
        c1.value = 123
        print(c1.value)

    def test_setFormula2(self):
        c1 = self.s.cell((1,1))
        c1.value=123
        c1.formula = "=SUM(A1:B3)"

    def test_value(self):
        c1 = DataCell(
            address = CellAddresses.fromColRow(1,1),
        )
        c1.value = 123
        self.assertTrue(isinstance(c1.value,int))
        print(c1.value)
