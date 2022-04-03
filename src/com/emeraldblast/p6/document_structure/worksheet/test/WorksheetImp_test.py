import random
import unittest
from unittest.mock import MagicMock

from com.emeraldblast.p6.document_structure.worksheet.WorksheetErrors import WorksheetErrors

from com.emeraldblast.p6.document_structure.cell.DataCell import DataCell
from com.emeraldblast.p6.document_structure.cell.address.CellIndex import CellIndex
from com.emeraldblast.p6.document_structure.formula_translator.FormulaTranslators import FormulaTranslators
from com.emeraldblast.p6.document_structure.range.RangeImp import RangeImp
from com.emeraldblast.p6.document_structure.range.address.RangeAddressImp import RangeAddressImp
from com.emeraldblast.p6.document_structure.workbook.WorkbookErrors import WorkbookErrors
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp
from com.emeraldblast.p6.document_structure.worksheet.WorksheetImp import WorksheetImp


class WorksheetImp_test(unittest.TestCase):

    def makeTestObj2(self):
        w1 = WorkbookImp("w1")
        s1 = w1.createNewWorksheet("s1")
        s2 = w1.createNewWorksheet("s2")
        s3 = w1.createNewWorksheet("s3")
        return s1, s2, s3, w1
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
        s = WorksheetImp(name = "oldName",workbook = wb)
        wb.addWorksheet(s)
        s.rename("newName")
        self.assertEqual("newName", s.name)

    def test_cell(self):
        s = WorksheetImp(name="s",workbook = MagicMock())
        expect = DataCell(CellIndex(1, 2))

        c1 = s.cell("@A2")
        self.assertEqual(expect, c1)

        c2 = s.cell("@a2")
        self.assertEqual(expect, c2)

        c3 = s.cell((1, 2))
        self.assertEqual(expect, c3)

    def test_range(self):
        s = WorksheetImp(name="s",workbook = MagicMock())
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
        s = WorksheetImp(name="s",workbook = MagicMock())
        self.assertFalse(s.hasCellAt(CellIndex(1, 1)))
        s.addCell(DataCell(CellIndex(1, 1), value = 123, script = "script"))
        self.assertTrue(s.hasCellAt(CellIndex(1, 1)))

    def test_getCell(self):
        s = WorksheetImp(name="s",workbook = MagicMock())
        cellAddr = CellIndex(12, 12)
        cell = DataCell(cellAddr, self.transGetterForCell)
        s.addCell(cell)
        self.assertEqual(cell, s.getOrMakeCell(cellAddr))

    def test_isEmpty(self):
        sheet = WorksheetImp(name="s", workbook = MagicMock())
        self.assertTrue(sheet.isEmpty())
        cell, cellAddr = self.makeTestObj()
        sheet.addCell(cell)
        self.assertFalse(sheet.isEmpty())
        sheet.removeCell(cellAddr)
        self.assertTrue(sheet.isEmpty())

    def test_containAddress(self):
        s = WorksheetImp(name="s",workbook = MagicMock())
        cell, cellAddr = self.makeTestObj()
        self.assertTrue(s.containsAddress(cellAddr))
        s.addCell(cell)
        self.assertTrue(s.containsAddress(cellAddr))
        s.removeCell(cellAddr)
        self.assertTrue(s.containsAddress(cellAddr))

    def test_cells(self):
        cell1, cellAddr1 = self.makeTestObj()
        cell2, cellAddr2 = self.makeTestObj()
        s = WorksheetImp(name="s",workbook = MagicMock())
        s.addCell(cell1)
        s.addCell(cell2)
        self.assertTrue(cell1 in s.cells)
        self.assertTrue(cell2 in s.cells)
        s.removeCell(cellAddr1)
        self.assertEqual([cell2], s.cells)

    def test_getNonExistenceCell(self):
        s = WorksheetImp(name="s",workbook = MagicMock())
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

    def test_RemoveCell(self):
        s = self.makeS()
        c = s.getOrMakeCell(CellIndex(1, 1))
        c.value = 123
        s.removeCell(CellIndex(1, 1))
        self.assertTrue(s.isEmpty())
        self.assertIsNone(s.getCell(CellIndex(1, 1)))

    def makeS(self):
        return WorksheetImp(name="s",workbook = MagicMock())
