import unittest
from collections import OrderedDict
from pathlib import Path

from bicp_document_structure.app.workbook_container.WorkbookContainerImp import WorkbookContainerImp
from bicp_document_structure.workbook.WorkbookFileInfoImp import WorkbookFileInfoImp
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp


class WorkbookContainerImp_test(unittest.TestCase):

    def makeTestObjs(self):
        d = OrderedDict({
            WorkbookFileInfoImp("b1",Path("p1")): WorkbookImp("b1"),
            WorkbookFileInfoImp("b2",Path("p1")): WorkbookImp("b2"),
            WorkbookFileInfoImp("b3",Path("p1")): WorkbookImp("b3"),
        })

        wbc2 = WorkbookContainerImp(d)
        return wbc2,d

    def test_constructor(self):
        wbc = WorkbookContainerImp()
        self.assertTrue(wbc.isEmpty())

        d = OrderedDict({
            WorkbookFileInfoImp("b1"):WorkbookImp("b1"),
            WorkbookFileInfoImp("b2"):WorkbookImp("b2")
        })

        wbc2 = WorkbookContainerImp(d)
        self.assertFalse(wbc2.isEmpty())

    def test_getWorkbook(self):
        self.test_getWorkbookByFileInfo()

    def test_createNewBook(self):
        wc,d = self.makeTestObjs()
        oldCount = len(d)
        wc.createNewWorkbook("bx")
        self.assertEqual(oldCount+1,len(d))

    def test_removeBook(self):
        wc,d = self.makeTestObjs()
        b2 = list(d.items())[1][1]
        b3 = list(d.items())[2][1]
        wc.removeWorkbook(0)
        self.assertEqual(2,len(d))

        self.assertEqual(b2,list(d.items())[0][1])
        self.assertEqual(b3,list(d.items())[1][1])

    def test_getWorkbookByIndex(self):
        wc, d = self.makeTestObjs()
        for x in range(len(d)):
            self.assertEqual(list(d.items())[x][1],wc.getWorkbookByIndex(x))
        with self.assertRaises(ValueError):
            wc.getWorkbookByIndex(1000)

    def test_getWorkbookByName(self):
        wc, d = self.makeTestObjs()
        names = list(map(lambda e:e[0].fileName,list(d.items())))
        for x,name in enumerate(names):
            self.assertEqual(list(d.items())[x][1],wc.getWorkbookByName(name))

        with self.assertRaises(ValueError):
            wc.getWorkbookByName("unavailableName")

    def test_getWorkbookByPath(self):
        wc,d = self.makeTestObjs()
        b1 = list(d.items())[0][1]
        self.assertEqual(b1,wc.getWorkbookByPath(Path("p1")))
        with self.assertRaises(ValueError):
            wc.getWorkbookByPath(Path("unavailablePath"))

    def test_getWorkbookByFileInfo(self):
        wc, d = self.makeTestObjs()
        b1 = wc.getWorkbook(WorkbookFileInfoImp("b1",Path("p1")))
        self.assertIsNotNone(b1)
        self.assertEqual(list(d.items())[0][1], b1)

        with self.assertRaises(ValueError):
            wc.getWorkbook(WorkbookFileInfoImp("bx"))