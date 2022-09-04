import unittest
from pathlib import Path

from com.qxdzbc.p6.document_structure.app.run_result.SingleResultDict import SingleResultDict
from com.qxdzbc.p6.document_structure.cell.address.CellIndex import CellIndex
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeyImp import WorkbookKeyImp


class RunResultImpTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.dict = {}
        self.srd = SingleResultDict(self.dict)

    def test_add(self):
        wbkey = WorkbookKeyImp("k1",Path("p1"))
        sheetName = "ws1"
        cell = CellIndex(1,1)
        self.srd.add(wbkey,sheetName,cell)
        self.assertEqual(1,len(self.dict))
        self.assertTrue(self.srd.checkContain(wbkey,sheetName,cell))
        self.assertTrue(self.srd.checkContain(wbkey, sheetName, CellIndex(1, 1)))
        self.assertTrue(self.srd.checkContain(WorkbookKeyImp("k1",Path("p1")), sheetName, CellIndex(1, 1)))
        self.assertFalse(self.srd.checkContain(wbkey,sheetName+"zzz",cell))
        self.assertFalse(self.srd.checkContain(wbkey,sheetName,CellIndex(1,2)))
        self.assertFalse(self.srd.checkContain(WorkbookKeyImp("k2",Path("zz")),sheetName,CellIndex(1,1)))

    def test_remove(self):
        wbkey = WorkbookKeyImp("k1", Path("p1"))
        sheetName = "ws1"
        cell = CellIndex(1, 1)
        cell2 = CellIndex(1,2)
        self.srd.add(wbkey, sheetName, cell)
        self.srd.add(wbkey, sheetName, cell2)
        # remove non-exist element
        self.srd.remove(wbkey,"nonExistSheet",cell)
        self.assertEqual(1,len(self.dict))

        # remove valid element
        self.srd.remove(wbkey,sheetName,cell)
        self.assertEqual(1, len(self.dict))
        self.assertTrue(self.srd.checkContain(wbkey,sheetName,cell2))
        self.assertFalse(self.srd.checkContain(wbkey,sheetName,cell))

        # remove everything
        self.srd.remove(wbkey, sheetName, cell2)
        self.assertEqual(0, len(self.dict))
        self.assertFalse(self.srd.checkContain(wbkey, sheetName, cell2))
        self.assertFalse(self.srd.checkContain(wbkey, sheetName, cell))

    def test_clear(self):
        wbkey = WorkbookKeyImp("k1", Path("p1"))
        sheetName = "ws1"
        cell = CellIndex(1, 1)
        cell2 = CellIndex(1, 2)
        self.srd.add(wbkey, sheetName, cell)
        self.srd.add(wbkey, sheetName, cell2)
        self.srd.clear()
        # remove everything
        self.assertFalse(self.srd.checkContain(wbkey, sheetName, cell2))
        self.assertFalse(self.srd.checkContain(wbkey, sheetName, cell))





