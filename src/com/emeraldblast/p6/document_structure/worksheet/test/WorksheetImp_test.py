import random
import unittest
from unittest.mock import MagicMock

import pyperclip

from com.emeraldblast.p6.document_structure.copy_paste.paster.Pasters import Pasters

from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy

from com.emeraldblast.p6.document_structure.cell.DataCell import DataCell
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.cell.address.CellIndex import CellIndex
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeId import RangeId
from com.emeraldblast.p6.document_structure.formula_translator.FormulaTranslators import FormulaTranslators
from com.emeraldblast.p6.document_structure.range.RangeImp import RangeImp
from com.emeraldblast.p6.document_structure.range.address.RangeAddressImp import RangeAddressImp
from com.emeraldblast.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.emeraldblast.p6.document_structure.util.for_test.TestUtils import TestErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.workbook.WorkbookErrors import WorkbookErrors
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.document_structure.worksheet.WorksheetErrors import WorksheetErrors
from com.emeraldblast.p6.document_structure.worksheet.WorksheetImp import WorksheetImp


class WorksheetImp_test(unittest.TestCase):

    def makeTestObj2(self):
        w1 = WorkbookImp("w1")
        s1 = w1.createNewWorksheet("s1")
        s2 = w1.createNewWorksheet("s2")
        s3 = w1.createNewWorksheet("s3")
        return s1, s2, s3, w1

    def setUp(self) -> None:
        super().setUp()
        s1, s2, s3, w1 = self.makeTestObj2()
        self.w1 = w1
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3

    def test_pasteText(self):
        paster = MagicMock()
        paster.pasteRange = MagicMock(return_value = Ok(RangeCopy(
            rangeId = None,
            cells = [
                DataCell(
                    address = None,
                    value = "abc"
                )
            ]
        )))
        self.s1.pasteTextRs(CellAddresses.fromLabel("@B9"),paster)
        self.assertEqual("abc",self.s1.cell("@B9").bareValue)
        paster.pasteRange = MagicMock(return_value = Ok(RangeCopy(
            rangeId = None,
            cells = [
                DataCell(
                    address = None,
                    formula="=SUM(A1:A9)"
                )
            ]
        )))
        self.s1.pasteTextRs(CellAddresses.fromLabel("@B9"), paster)
        self.assertEqual("=SUM(A1:A9)", self.s1.cell("@B9").bareFormula)

    def test_pasteProtoFromClipboardRs_ok(self):
        paster = MagicMock()
        rangeCopy = RangeCopy(
            rangeId = RangeId(
                rangeAddress = RangeAddresses.fromLabel("@D4:G10"),
                workbookKey = WorkbookKeys.fromNameAndPath(""),
                worksheetName = "s123"
            ),
            cells = [
                DataCell(
                    address = CellAddresses.fromLabel("@D6"),
                    value = 11
                ),
                DataCell(
                    address = CellAddresses.fromLabel("@E8"),
                    value = 23,
                ),
                DataCell(
                    address = CellAddresses.fromLabel("@G7"),
                    value = None,
                    formula = "=SUM(D5:E8)"
                )
            ]
        )
        s = WorksheetImp("ASD", MagicMock())
        paster.pasteRange = MagicMock(return_value = Ok(rangeCopy))
        rs=s.pasteProtoRs(
            anchorCell = CellAddresses.fromLabel("@M13"),
            paster = paster
        )
        self.assertTrue(rs.isOk())
        self.assertEqual(11, s.cell("@M15").value)
        self.assertEqual(23, s.cell("@N17").value)
        self.assertEqual("=SUM(D5:E8)", s.cell("@P16").formula)

    def test_pasteProtoFromClipboardRs_err(self):
        paster = MagicMock()
        s = WorksheetImp("ASD", MagicMock())
        paster.pasteRange = MagicMock(return_value = Err(TestErrorReport))
        rs = s.pasteProtoRs(
            anchorCell = CellAddresses.fromLabel("@M13"),
            paster = paster
        )
        self.assertTrue(rs.isErr())
    def test_pasteProtoFromClipboardRs_err2(self):
        content = b"abc"
        pyperclip.copy(str(content))
        s = WorksheetImp("ASD", MagicMock())
        rs = s.pasteProtoRs(
            anchorCell = CellAddresses.fromLabel("@M13"),
            paster = Pasters.protoPaster
        )
        self.assertTrue(rs.isErr())
        print(str(rs.err))

    def test_update_usedRange_when_update_cell(self):
        self.assertIsNone(self.s1.usedRangeAddress)
        self.assertIsNone(self.s1.usedRange)

        self.s1.cell((1, 1)).value = 123
        self.assertEqual(RangeAddresses.fromColRow(1, 1, 1, 1), self.s1.usedRangeAddress)
        self.s1.cell((2, 2)).value = 123
        self.assertEqual(RangeAddresses.fromColRow(1, 2, 1, 2), self.s1.usedRangeAddress)
        self.s1.cell((2, 100)).value = 123

        self.assertEqual(RangeAddresses.fromColRow(1, 2, 1, 100), self.s1.usedRangeAddress)

        self.s1.cell((2, 12)).value = 123
        self.s1.cell((2, 22)).value = 123
        self.s1.cell((2, 32)).value = 123
        self.s1.cell((2, 42)).value = 123
        self.s1.cell((2, 52)).value = 123
        self.s1.deleteCell((2, 100))
        self.assertEqual(RangeAddresses.fromColRow(1, 2, 1, 52), self.s1.usedRangeAddress)

        self.s1.deleteRangeRs(RangeAddresses.fromColRow(2, 2, 12, 22))
        self.assertEqual(RangeAddresses.fromColRow(1, 2, 1, 52), self.s1.usedRangeAddress)

        self.s1.deleteRangeRs(RangeAddresses.fromColRow(2, 2, 42, 52))
        self.assertEqual(RangeAddresses.fromColRow(1, 2, 1, 32), self.s1.usedRangeAddress)

        self.s1.cell((10, 3)).value = 123
        self.assertEqual(RangeAddresses.fromColRow(1, 10, 1, 32), self.s1.usedRangeAddress)
        self.s1.deleteRange(RangeAddresses.fromColRow(5, 11, 1, 3))
        print(self.s1.usedRangeAddress)
        self.assertEqual(RangeAddresses.fromColRow(1, 2, 1, 32), self.s1.usedRangeAddress)

    def test_qwe(self):
        s1 = self.s1

        s1.cell((1, 1)).formula = "11"
        self.assertEqual(11, s1.cell((1, 1)).value)

        s1.cell((1, 1)).formula = "abc"
        self.assertEqual("abc", s1.cell((1, 1)).value)

        s1.cell((1, 1)).formula = "=1+1"
        self.assertEqual(2, s1.cell((1, 1)).value)

    def test_pasteDataFrame(self):
        s1 = self.s1
        s2 = self.s2
        s1.cell((1, 1)).value = 11
        s1.cell((1, 2)).formula = "=SCRIPT(1+2)"
        s1.cell((4, 6)).script = "1+2+3"

        rangeS1 = RangeImp(
            firstCellAddress = CellAddresses.fromColRow(1, 1),
            lastCellAddress = CellAddresses.fromColRow(5, 6),
            sourceContainer = s1
        )
        rangeS1.copySourceValueDataFrame()
        self.assertEqual(0, s2.size)
        anchorCell = CellAddresses.fromColRow(2, 4)
        rs = s2.pasteDataFrameRs(anchorCell)
        self.assertTrue(rs.isOk())
        self.assertEqual(3, s2.size)
        self.assertEqual(
            s1.cell((1, 1)).value,
            s2.cell((1 + 2 - 1, 1 + 4 - 1)).value
        )

        self.assertEqual(
            s1.cell((1, 2)).formula,
            s2.cell((1 + 2 - 1, 2 + 4 - 1)).formula,
        )

        self.assertEqual(
            s1.cell((4, 6)).script,
            s2.cell((4 + 2 - 1, 6 + 4 - 1)).script,
        )

    def test_deleteRange(self):
        self.s1.cell("@A1").value = "a1"
        self.s1.cell("@A2").value = "a2"
        self.s1.cell("@A3").value = "a3"
        self.s1.cell("@B2").value = "b2"
        r1 = RangeAddresses.from2Cells(CellAddresses.fromLabel("@A1"), CellAddresses.fromLabel("@B2"))
        rs = self.s1.deleteRangeRs(r1)
        self.assertTrue(rs.isOk())
        self.assertFalse(self.s1.hasCellAt(CellAddresses.fromLabel("@A1")))
        self.assertFalse(self.s1.hasCellAt(CellAddresses.fromLabel("@A2")))
        self.assertFalse(self.s1.hasCellAt(CellAddresses.fromLabel("@B2")))
        self.assertTrue(self.s1.hasCellAt(CellAddresses.fromLabel("@A3")))

    def test_rename(self):
        s1, s2, s3, w = self.makeTestObj2()
        oldName = s1.name
        newName = "newS1"
        s1.rename(newName)
        self.assertEqual(newName, s1.name)
        self.assertIsNone(w.getWorksheetOrNone(oldName))
        self.assertIsNotNone(w.getWorksheetOrNone(newName))
        with self.assertRaises(Exception):
            self.assertIsNone(w.getTranslator(oldName))
        self.assertIsNotNone(w.getTranslator(newName))
        self.assertIsNotNone(s1.translator)
        # ensure that sheet index is not changed after name changed
        self.assertEqual(w.getWorksheetByIndex(0).name, newName)

    #
    def test_renameWorksheetRs_Ok(self):
        s1, s2, s3, w = self.makeTestObj2()
        newName = "newS1"
        rs = s1.renameRs(newName)
        self.assertTrue(rs.isOk())
        self.assertEqual(newName, s1.name, "Worksheet name is not the new name")
        self.assertEqual(s1, w.getWorksheet(0), "Worksheet index was affected by changing name")

    def test_renameWorksheetRs_InvalidNewName(self):
        s1, s2, s3, w = self.makeTestObj2()
        rs = s1.renameRs("")
        self.assertTrue(rs.isErr())
        self.assertEqual(WorksheetErrors.IllegalNameReport.header, rs.err.header, "incorrect error header")
        self.assertEqual("", rs.err.data.name, "incorrect error data")

    #
    def test_renameWorksheetRs_NameOfOtherSheet(self):
        s1, s2, s3, w = self.makeTestObj2()
        rs = s1.renameRs(s2.name)
        self.assertTrue(rs.isErr())
        self.assertEqual(WorkbookErrors.WorksheetAlreadyExistReport.header, rs.err.header, "incorrect error header")
        self.assertEqual(s2.name, rs.err.data.name, "incorrect error data")

    #
    def test_renameWorksheetRs_SameName(self):
        s1, s2, s3, w = self.makeTestObj2()
        rs = s1.renameRs(s1.name)
        self.assertTrue(rs.isOk())

    def test_toProtoObj(self):
        s = WorksheetImp(name = "oldName", workbook = MagicMock())
        s.cell("@A1").value = 123
        s.cell("@B3").value = 333
        o = s.toProtoObj()
        self.assertEqual("oldName", o.name)
        self.assertEqual(s.cell("@A1").toProtoObj(), o.cell[0])
        self.assertEqual(s.cell("@B3").toProtoObj(), o.cell[1])
        print(s)

    @staticmethod
    def transGetter(name):
        return FormulaTranslators.mock()

    def testRename(self):
        wb = WorkbookImp("w")
        s = WorksheetImp(name = "oldName", workbook = wb)
        wb.addWorksheet(s)
        s.rename("newName")
        self.assertEqual("newName", s.name)

    def test_cell(self):
        s = WorksheetImp(name = "s", workbook = MagicMock())
        expect = DataCell(CellIndex(1, 2))

        c1 = s.cell("@A2")
        self.assertEqual(expect, c1)

        c2 = s.cell("@a2")
        self.assertEqual(expect, c2)

        c3 = s.cell((1, 2))
        self.assertEqual(expect, c3)

    def test_range(self):
        s = WorksheetImp(name = "s", workbook = MagicMock())
        ad1 = CellIndex(1, 1)  # A1
        ad2 = CellIndex(20, 20)  # T20
        expect = RangeImp(ad1, ad2, s)

        r1 = s.range("@A1:T20")
        self.assertEqual(expect, r1)

        r2 = s.range(RangeAddressImp(ad1, ad2))
        self.assertEqual(expect, r2)

        r3 = s.range((ad1, ad2))
        self.assertEqual(expect, r3)

    def transGetterForCell(self):
        return FormulaTranslators.mock()

    def makeTestObj(self):
        cellAddr = CellIndex(random.randrange(1, 20), random.randrange(1, 20))
        cell = DataCell(cellAddr, value = 123, script = "script")
        return cell, cellAddr

    def test_hasCellAt(self):
        s = WorksheetImp(name = "s", workbook = MagicMock())
        self.assertFalse(s.hasCellAt(CellIndex(1, 1)))
        s.addCell(DataCell(CellIndex(1, 1), value = 123, script = "script"))
        self.assertTrue(s.hasCellAt(CellIndex(1, 1)))

    def test_getCell(self):
        s = WorksheetImp(name = "s", workbook = MagicMock())
        cellAddr = CellIndex(12, 12)
        cell = DataCell(cellAddr, self.transGetterForCell)
        s.addCell(cell)
        self.assertEqual(cell, s.getOrMakeCell(cellAddr))

    def test_isEmpty(self):
        sheet = WorksheetImp(name = "s", workbook = MagicMock())
        self.assertTrue(sheet.isEmpty())
        cell, cellAddr = self.makeTestObj()
        sheet.addCell(cell)
        self.assertFalse(sheet.isEmpty())
        sheet.deleteCell(cellAddr)
        self.assertTrue(sheet.isEmpty())

    def test_containAddress(self):
        s = WorksheetImp(name = "s", workbook = MagicMock())
        cell, cellAddr = self.makeTestObj()
        self.assertTrue(s.containsAddress(cellAddr))
        s.addCell(cell)
        self.assertTrue(s.containsAddress(cellAddr))
        s.deleteCell(cellAddr)
        self.assertTrue(s.containsAddress(cellAddr))

    def test_cells(self):
        cell1, cellAddr1 = self.makeTestObj()
        cell2, cellAddr2 = self.makeTestObj()
        s = WorksheetImp(name = "s", workbook = MagicMock())
        s.addCell(cell1)
        s.addCell(cell2)
        self.assertTrue(cell1 in s.cells)
        self.assertTrue(cell2 in s.cells)
        s.deleteCell(cellAddr1)
        self.assertEqual([cell2], s.cells)

    def test_getNonExistenceCell(self):
        s = WorksheetImp(name = "s", workbook = MagicMock())
        c = s.getOrMakeCell(CellIndex(1, 1))
        self.assertIsNotNone(c)
        self.assertTrue(s.isEmpty())
        c.script = "z"
        self.assertFalse(s.isEmpty())

        c2Addr = CellIndex(1, 2)
        c2 = s.getOrMakeCell(c2Addr)
        self.assertFalse(s.hasCellAt(c2Addr))
        c2.value = 123
        self.assertTrue(s.hasCellAt(c2Addr))

    def test_deleteCell(self):
        s = self.makeS()
        c = s.getOrMakeCell(CellIndex(1, 1))
        c.value = 123
        s.deleteCell(CellIndex(1, 1))
        self.assertTrue(s.isEmpty())
        self.assertIsNone(s.getCell(CellIndex(1, 1)))

    def makeS(self):
        return WorksheetImp(name = "s", workbook = MagicMock())
