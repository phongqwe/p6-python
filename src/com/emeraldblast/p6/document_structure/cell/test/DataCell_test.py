import unittest

from com.emeraldblast.p6.document_structure.cell.DataCell import DataCell
from com.emeraldblast.p6.document_structure.cell.EventCell import EventCell
from com.emeraldblast.p6.document_structure.cell.address.CellIndex import CellIndex
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.CellEventData import CellEventData
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp
from com.emeraldblast.p6.proto.DocProtos_pb2 import CellProto


class DataCellTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.wb = WorkbookImp("wb")
        self.s = self.wb.createNewWorksheet("s1")


    def test_toProtoObj1(self):
        c1 = DataCell(CellIndex(1, 1), 123, "formula", "script")
        o = c1.toProtoObj()
        self.assertEqual(c1.address.toProtoObj(), o.address)
        self.assertEqual("123", o.displayValue)
        self.assertEqual("script", o.script)
        self.assertEqual("formula", o.formula)

    def test_toProtoObj2(self):

        c1 = DataCell(CellIndex(1, 1))
        o = c1.toProtoObj()
        self.assertEqual(c1.address.toProtoObj(), o.address)
        self.assertEqual("", o.displayValue)
        self.assertEqual("", o.script)
        self.assertEqual("", o.formula)
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

        def increaseExCount(eventData:CellEventData):
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

        def increaseExCount(data:CellEventData):
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
        c.value
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

    # def test_formula_setter(self):
    #     c1 = self.s.cell((1,1))
    #     c1.value=123
    #     c1.script = "x=1;y=x*2+3;y"
    #     print(c1.value)
        # with self.assertRaises(Exception):
        #     c1.formula = "new formula"

    def test_setFormula1(self):
        c1 = self.s.cell((1, 1))
        c1.value = 123
        c1.script = "x=1;y=x*2+3;y"
        c1.formula = "=SCRIPT(x=1;y=x-200;y)"
        self.assertEqual("x=1;y=x-200;y", c1.script)
        self.assertEqual(-199, c1.value)
        print(c1.value)

    def test_setFormula2(self):
        c1 = self.s.cell((1,1))
        c1.value=123
        c1.script="x=1;y=x*2+3;y"
        c1.formula = "=SUM(A1:B3)"
        self.assertEqual(
            """WorksheetFunctions.SUM(getWorkbook(WorkbookKeys.fromNameAndPath("wb",None)).getWorksheet("s1").range(\"@A1:B3\"))""",
            c1.script)
        c1.script = "x=99;y=x-200;y"
        self.assertEqual("=SCRIPT(x=99;y=x-200;y)", c1.formula)
