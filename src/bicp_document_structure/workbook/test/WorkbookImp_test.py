import unittest
from collections import OrderedDict

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.formula_translator.FormulaTranslators import FormulaTranslators
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp
from bicp_document_structure.worksheet.Worksheet import Worksheet
from bicp_document_structure.worksheet.WorksheetImp2 import WorksheetImp2


class WorkbookImp_test(unittest.TestCase):

    @staticmethod
    def transGetter(name):
        return FormulaTranslators.mock()
    def makeTestObj(self):
        s1 = WorksheetImp2(name="s1",translatorGetter = self.transGetter)
        s2 = WorksheetImp2(name="s2",translatorGetter = self.transGetter)
        s3 = WorksheetImp2(name="s3",translatorGetter = self.transGetter)
        d = OrderedDict({
            s1.name: s1,
            s2.name: s2,
            s3.name: s3
        })
        w1 = WorkbookImp("w1", sheetDict = d)
        return s1, s2, s3, w1, d

    def test_constructor(self):
        s1, s2, s3, w, sheetDict = self.makeTestObj()
        d = OrderedDict({
            s1.name: s1,
            s2.name: s2,
        })
        w1 = WorkbookImp("w1", sheetDict = d)
        self.assertFalse(w1.isEmpty())
        self.assertEqual(2, w1.sheetCount)
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
        self.assertEqual(s4, sheetDict["s4"])

        with self.assertRaises(ValueError):
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
        s1, s2, s3, w1, d=self.makeTestObj()
        expect = """{"name": "w1", "path": null, "worksheets": [{"name": "s1", "cells": []}, {"name": "s2", "cells": []}, {"name": "s3", "cells": []}]}"""
        self.assertEqual(expect,w1.toJsonStr())
        # print(w1.toJsonStr())