import unittest
from collections import OrderedDict
from pathlib import Path

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.formula_translator.FormulaTranslators import FormulaTranslators
from bicp_document_structure.communication.event.P6Event import P6Event
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookErrors import WorkbookErrors
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp
from bicp_document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from bicp_document_structure.worksheet.Worksheet import Worksheet
from bicp_document_structure.worksheet.WorksheetErrors import WorksheetErrors
from bicp_document_structure.worksheet.WorksheetImp import WorksheetImp


class WorkbookImp_test(unittest.TestCase):

    def test_toProtoObj(self):
        s1, s2, s3, w1, d = self.makeTestObj()
        o = w1.toProtoObj()
        self.assertEqual(w1.name, o.workbookKey.name)
        self.assertEqual("null", o.workbookKey.path.WhichOneof("kind"))
        self.assertEqual(s1.toProtoObj(), o.worksheet[0])
        self.assertEqual(s2.toProtoObj(), o.worksheet[1])
        self.assertEqual(s3.toProtoObj(), o.worksheet[2])
        w1.path = Path("someFile.qwe")
        o2 = w1.toProtoObj()
        self.assertEqual("str", o2.workbookKey.path.WhichOneof("kind"))
        self.assertEqual(str(w1.path.absolute()), o2.workbookKey.path.str)

    @staticmethod
    def transGetter(name):
        return FormulaTranslators.mock()

    def makeTestObj(self):
        s1 = WorksheetImp(name = "s1", translatorGetter = self.transGetter)
        s2 = WorksheetImp(name = "s2", translatorGetter = self.transGetter)
        s3 = WorksheetImp(name = "s3", translatorGetter = self.transGetter)
        d = [s1,s2,s3]
        w1 = WorkbookImp("w1", sheetList = d)
        return s1, s2, s3, w1, d

    def test_rename(self):
        s1, s2, s3, w, sheetList = self.makeTestObj()
        oldName = s1.name
        newName = "newS1"
        w.renameWorksheet(s1.name, newName)
        self.assertEqual(newName, s1.name)
        self.assertIsNone(w.getWorksheetOrNone(oldName))
        self.assertIsNotNone(w.getWorksheetOrNone(newName))
        with self.assertRaises(Exception):
            self.assertIsNone(w.getTranslator(oldName))
        self.assertIsNotNone(w.getTranslator(newName))
        self.assertIsNotNone(s1.translator)
        # ensure that sheet index is not changed after name changed
        self.assertEqual(w.getWorksheetByIndex(0).name, newName)

    def test_renameWorksheetRs_Ok(self):
        s1, s2, s3, w, sheetDict = self.makeTestObj()
        oldName = s1.name
        newName = "newS1"
        rs = w.renameWorksheetRs(s1.name, newName)
        self.assertTrue(rs.isOk())
        self.assertEqual(newName, s1.name, "Worksheet name is not the new name")
        self.assertEqual(s1, w.getWorksheet(0), "Worksheet index was affected by changing name")

    def test_renameWorksheetRs_InvalidTarget(self):
        s1, s2, s3, w, sheetDict = self.makeTestObj()
        rs = w.renameWorksheetRs("invalid name", "new Name")
        self.assertTrue(rs.isErr())
        self.assertEqual(WorkbookErrors.WorksheetNotExistReport.header, rs.err.header, "incorrect error header")
        self.assertEqual("invalid name", rs.err.data.name, "incorrect error data")

    def test_renameWorksheetRs_InvalidNewName(self):
        s1, s2, s3, w, sheetDict = self.makeTestObj()
        rs = w.renameWorksheetRs(s1.name,"")
        self.assertTrue(rs.isErr())
        self.assertEqual(WorksheetErrors.IllegalNameReport.header, rs.err.header, "incorrect error header")
        self.assertEqual("", rs.err.data.name, "incorrect error data")

    def test_renameWorksheetRs_NameOfOtherSheet(self):
        s1, s2, s3, w, sheetDict = self.makeTestObj()
        rs = w.renameWorksheetRs(s1.name,s2.name)
        self.assertTrue(rs.isErr())
        self.assertEqual(WorkbookErrors.WorksheetAlreadyExistReport.header, rs.err.header, "incorrect error header")
        self.assertEqual(s2.name, rs.err.data.name, "incorrect error data")

    def test_renameWorksheetRs_SameName(self):
        s1, s2, s3, w, sheetDict = self.makeTestObj()
        rs = w.renameWorksheetRs(s1.name,s1.name)
        self.assertTrue(rs.isOk())

    def test_constructor(self):
        s1, s2, s3, w, sheetDict = self.makeTestObj()
        d = [s1,s2,s3]
        w1 = WorkbookImp("w1", sheetList = d)
        self.assertFalse(w1.isEmpty())
        self.assertEqual(3, w1.sheetCount)
        self.assertEqual(s1, w1.getWorksheetByName(s1.name))
        self.assertEqual(s2, w1.getWorksheetByName(s2.name))

    def test_fromSheets(self):
        s1, s2, s3, w1, sheetDict = self.makeTestObj()
        self.assertEqual(s1, w1.getWorksheetByName(s1.name))
        self.assertEqual(s2, w1.getWorksheetByName(s2.name))
        self.assertEqual(s3, w1.getWorksheetByName(s3.name))

    def test_getSheetByName(self):
        self.test_fromSheets()

    def test_getSheetByIndex(self):
        s1, s2, s3, w1, sheetDict = self.makeTestObj()
        self.assertEqual(s1, w1.getWorksheetByIndex(0))
        self.assertEqual(s2, w1.getWorksheetByIndex(1))
        self.assertEqual(s3, w1.getWorksheetByIndex(2))

    def test_getSheet(self):
        s1, s2, s3, w1, sheetDict = self.makeTestObj()

        self.assertEqual(s1, w1.getWorksheet(0))
        self.assertEqual(s1, w1.getWorksheet(s1.name))

        self.assertEqual(s2, w1.getWorksheet(1))
        self.assertEqual(s2, w1.getWorksheet(s2.name))

        self.assertEqual(s3, w1.getWorksheet(2))
        self.assertEqual(s3, w1.getWorksheet(s3.name))

    def test_sheetCount(self):
        s1, s2, s3, w1, sheetDict = self.makeTestObj()
        self.assertEqual(len(sheetDict), w1.sheetCount)
        w1.removeWorksheetByIndex(0)
        self.assertEqual(2, w1.sheetCount)

    def test_createNameSheet(self):
        s1, s2, s3, w1, sheetDict = self.makeTestObj()

        s4 = w1.createNewWorksheet("s4")
        self.assertEqual(s4, w1.getWorksheet("s4"))

        with self.assertRaises(Exception):
            w1.createNewWorksheet("s1")

    def test_CreateNewSheet_autoNaming(self):
        book = WorkbookImp("book")
        self.assertTrue(book.isEmpty())
        createRs = book.createNewWorksheetRs()
        self.assertTrue(createRs.isOk())
        self.assertTrue(not book.isEmpty())
        self.assertIsNotNone(book.getWorksheet("Sheet0"))
        book.createNewWorksheetRs()
        self.assertIsNotNone(book.getWorksheet("Sheet1"))

    def test_removeSheetByName(self):
        s1, s2, s3, w1, sheetDict = self.makeTestObj()
        ds = w1.removeWorksheetByName(s2.name)
        self.assertEqual(s2, ds)
        self.assertEqual(2, w1.sheetCount)
        self.assertEqual(s3, w1.getWorksheet(1))

    def test_removeSheetByIndex(self):
        s1, s2, s3, w1, sheetDict = self.makeTestObj()
        ds = w1.removeWorksheetByIndex(1)
        self.assertEqual(s2, ds)
        self.assertEqual(2, w1.sheetCount)
        self.assertEqual(s3, w1.getWorksheet(1))

    def test_removeSheet(self):
        s1, s2, s3, w1, sheetDict = self.makeTestObj()
        ds2 = w1.removeWorksheet(s2.name)
        self.assertEqual(s2, ds2)
        self.assertEqual(2, w1.sheetCount)
        self.assertEqual(s3, w1.getWorksheet(1))

        ds1 = w1.removeWorksheet(0)
        self.assertEqual(s1, ds1)
        self.assertEqual(1, w1.sheetCount)
        self.assertEqual(s3, w1.getWorksheet(0))
        with self.assertRaises(ValueError):
            w1.removeWorksheet(0.0)

    def test_activeSheet(self):
        s1, s2, s3, w1, sheetDict = self.makeTestObj()
        self.assertEqual(s1, w1.activeWorksheet)
        w1.setActiveWorksheet(1)
        self.assertEqual(s2, w1.activeWorksheet)
        w1.setActiveWorksheet(s3.name)
        self.assertEqual(s3, w1.activeWorksheet)
        with self.assertRaises(ValueError):
            w1.setActiveWorksheet(100)
        self.assertEqual(s3, w1.activeWorksheet)

    def test_listWorksheet(self):
        s1, s2, s3, w1, sheetDict = self.makeTestObj()
        print(w1.listWorksheet())

    def __onCellChange(self, wb: Workbook, ws: Worksheet, cell: Cell, event: P6Event):
        self.aa = f"{wb.name}, {ws.name}, {cell.address.label}, {event.code}"

    def __onCellChange2(self, wb: Workbook, ws: Worksheet, cell: Cell, event: P6Event):
        self.aa = f"{cell.address.label}"

    def test_toJson(self):
        s1, s2, s3, w1, d = self.makeTestObj()
        expect = """{"name": "w1", "path": null, "worksheets": [{"name": "s1", "cells": []}, {"name": "s2", "cells": []}, {"name": "s3", "cells": []}]}"""
        self.assertEqual(expect, w1.toJsonStr())
        print(w1.toJsonStr())

    def test_translator_when_change_key(self):
        # when a workbook change its path, translators of its children obj (sheets, cells) must be regenerated.
        w1 = WorkbookImp("w1", path = Path("p1"))
        s1 = w1.createNewWorksheet("s1")
        c1 = s1.cell("@A1")
        f = """=SUM(B3:B5)"""
        c1.formula = f

        outputTemplate = """WorksheetFunctions.SUM(getWorkbook(WorkbookKeys.fromNameAndPath("{bookName}","{bookPath}")).getWorksheet("{sheetName}").range("@B3:B5"))"""
        self.assertEqual(
            outputTemplate.format(bookName = "w1", bookPath = "p1", sheetName = "s1"),
            c1.script)
        w1.workbookKey = WorkbookKeys.fromNameAndPath(w1.name, "newPath")
        self.assertEqual(
            outputTemplate.format(bookName = "w1", bookPath = "newPath", sheetName = "s1"),
            c1.script)

        w1.name = "newBook"
        self.assertEqual(
            outputTemplate.format(bookName = "newBook", bookPath = "newPath", sheetName = "s1"),
            c1.script)
