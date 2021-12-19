import unittest
from collections import OrderedDict

from bicp_document_structure.sheet.WorksheetImp import WorksheetImp
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp


class WorkbookImp_test(unittest.TestCase):
    def makeTestObj(self):
        s1 = WorksheetImp("s1")
        s2 = WorksheetImp("s2")
        s3 = WorksheetImp("s3")
        d = OrderedDict({
            s1.name: s1,
            s2.name: s2,
            s3.name:s3
        })
        w1 = WorkbookImp("w1",d)
        return s1,s2,s3,w1,d

    def test_constructor(self):
        s1,s2,s3,w,sheetDict = self.makeTestObj()
        d = OrderedDict({
            s1.name:s1,
            s2.name:s2,
        })
        w1 = WorkbookImp("w1",d)
        self.assertFalse(w1.isEmpty())
        self.assertEqual(2,w1.sheetCount)
        self.assertEqual(s1,w1.getSheetByName(s1.name))
        self.assertEqual(s2,w1.getSheetByName(s2.name))


    def test_fromSheets(self):
        s1, s2, s3,w1,sheetDict = self.makeTestObj()
        self.assertEqual(s1, w1.getSheetByName(s1.name))
        self.assertEqual(s2, w1.getSheetByName(s2.name))
        self.assertEqual(s3, w1.getSheetByName(s3.name))

    def test_getSheetByName(self):
        self.test_fromSheets()

    def test_getSheetByIndex(self):
        s1, s2, s3,w1,sheetDict = self.makeTestObj()
        self.assertEqual(s1, w1.getSheetByIndex(0))
        self.assertEqual(s2, w1.getSheetByIndex(1))
        self.assertEqual(s3, w1.getSheetByIndex(2))

    def test_getSheet(self):
        s1, s2, s3,w1,sheetDict = self.makeTestObj()

        self.assertEqual(s1, w1.getSheet(0))
        self.assertEqual(s1, w1.getSheet(s1.name))

        self.assertEqual(s2, w1.getSheet(1))
        self.assertEqual(s2, w1.getSheet(s2.name))

        self.assertEqual(s3, w1.getSheet(2))
        self.assertEqual(s3, w1.getSheet(s3.name))

    def test_sheetCount(self):
        s1, s2, s3, w1,sheetDict = self.makeTestObj()
        self.assertEqual(len(sheetDict),w1.sheetCount)
        w1.removeSheetByIndex(0)
        self.assertEqual(2,w1.sheetCount)

    def test_createNameSheet(self):
        s1, s2, s3, w1, sheetDict = self.makeTestObj()

        s4 = w1.createNewSheet("s4")
        self.assertEqual(s4,w1.getSheet("s4"))
        self.assertEqual(s4,sheetDict["s4"])

        with self.assertRaises(ValueError):
            w1.createNewSheet("s1")

    def test_removeSheetByName(self):
        s1, s2, s3, w1, sheetDict = self.makeTestObj()
        ds = w1.removeSheetByName(s2.name)
        self.assertEqual(s2,ds)
        self.assertEqual(2,w1.sheetCount)
        self.assertEqual(s3,w1.getSheet(1))

    def test_removeSheetByIndex(self):
        s1, s2, s3, w1, sheetDict = self.makeTestObj()
        ds = w1.removeSheetByIndex(1)
        self.assertEqual(s2, ds)
        self.assertEqual(2, w1.sheetCount)
        self.assertEqual(s3, w1.getSheet(1))

    def test_removeSheet(self):
        s1, s2, s3, w1, sheetDict = self.makeTestObj()
        ds2 = w1.removeSheet(s2.name)
        self.assertEqual(s2, ds2)
        self.assertEqual(2, w1.sheetCount)
        self.assertEqual(s3, w1.getSheet(1))

        ds1 = w1.removeSheet(0)
        self.assertEqual(s1,ds1)
        self.assertEqual(1, w1.sheetCount)
        self.assertEqual(s3, w1.getSheet(0))
        with self.assertRaises(ValueError):
            w1.removeSheet(0.0)

    def test_activeSheet(self):
        s1, s2, s3, w1, sheetDict = self.makeTestObj()
        self.assertEqual(s1,w1.activeSheet)
        w1.setActiveSheet(1)
        self.assertEqual(s2, w1.activeSheet)
        w1.setActiveSheet(s3.name)
        self.assertEqual(s3, w1.activeSheet)
        with self.assertRaises(ValueError):
            w1.setActiveSheet(100)
        self.assertEqual(s3, w1.activeSheet)