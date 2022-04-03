import unittest
from collections import OrderedDict
from pathlib import Path

from com.emeraldblast.p6.document_structure.app.workbook_container.WorkbookContainerImp import WorkbookContainerImp
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeyImp import WorkbookKeyImp


class WorkbookContainerImp_test(unittest.TestCase):

    def makeTestObjs(self):
        d = OrderedDict({
            WorkbookKeyImp("b1", Path("p1")): WorkbookImp("b1",path=Path("p1")),
            WorkbookKeyImp("b2", Path("p1")): WorkbookImp("b2",path=Path("p2")),
            WorkbookKeyImp("b3", Path("p1")): WorkbookImp("b3",path=Path("p3")),
        })

        wbc2 = WorkbookContainerImp(d)
        return wbc2,d

    def test_constructor(self):
        wbc = WorkbookContainerImp()
        self.assertTrue(wbc.isEmpty())

        d = OrderedDict({
            WorkbookKeyImp("b1"):WorkbookImp("b1"),
            WorkbookKeyImp("b2"):WorkbookImp("b2")
        })

        wbc2 = WorkbookContainerImp(d)
        self.assertFalse(wbc2.isEmpty())

    def test_getWorkbook(self):
        self.test_getWorkbookByKey()
        self.test_getWorkbookByIndex()
        self.test_getWorkbookByName()

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
        self.assertIsNone(wc.getWorkbookByIndex(1000))

    def test_getWorkbookByName(self):
        wc, d = self.makeTestObjs()
        names = list(map(lambda e:e[0].fileName,list(d.items())))
        for x,name in enumerate(names):
            self.assertEqual(list(d.items())[x][1],wc.getWorkbookByName(name))
        self.assertIsNone(wc.getWorkbookByName("unavailableName"))

    def test_getWorkbookByPath(self):
        wc,d = self.makeTestObjs()
        b1 = list(d.items())[0][1]
        self.assertEqual(b1,wc.getWorkbookByPath(Path("p1")))
        self.assertIsNone(wc.getWorkbookByPath(Path("unavailablePath")))

    def test_getWorkbookByKey(self):
        wc, d = self.makeTestObjs()
        b1 = wc.getWorkbookByKey(WorkbookKeyImp("b1", Path("p1")))
        self.assertIsNotNone(b1)
        self.assertEqual(list(d.items())[0][1], b1)
        self.assertIsNone(wc.getWorkbookByKey(WorkbookKeyImp("bx")))