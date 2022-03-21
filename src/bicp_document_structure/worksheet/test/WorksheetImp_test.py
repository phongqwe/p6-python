import random
import unittest
from functools import partial
from unittest.mock import MagicMock

from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.formula_translator.FormulaTranslators import FormulaTranslators
from bicp_document_structure.range.RangeImp import RangeImp
from bicp_document_structure.range.address.RangeAddressImp import RangeAddressImp
from bicp_document_structure.worksheet.WorksheetImp import WorksheetImp


class WorksheetImp_test(unittest.TestCase):

    def test_toProtoObj(self):
        s = WorksheetImp(translatorGetter = MagicMock(), name = "oldName")
        s.cell("@A1").value=123
        s.cell("@B3").value=333
        o = s.toProtoObj()
        self.assertEqual("oldName",o.name)
        self.assertEqual(s.cell("@A1").toProtoObj(),o.cell[0])
        self.assertEqual(s.cell("@B3").toProtoObj(),o.cell[1])
        print(s.toProtoStr())

    @staticmethod
    def transGetter(name):
        return FormulaTranslators.mock()

    def testRename(self):
        s = WorksheetImp(translatorGetter = self.transGetter,name="oldName")
        s.rename("newName")
        self.assertEqual("newName",s.name)

    def test_cell(self):
        s = WorksheetImp(translatorGetter = self.transGetter)
        expect = DataCell(CellIndex(1, 2), translatorGetter = partial(self.transGetter, s.name))

        c1 = s.cell("@A2")
        self.assertEqual(expect, c1)

        c2 = s.cell("@a2")
        self.assertEqual(expect, c2)

        c3 = s.cell((1, 2))
        self.assertEqual(expect, c3)

    def test_range(self):
        s = WorksheetImp(translatorGetter = self.transGetter)
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
        cell = DataCell(cellAddr, translatorGetter = self.transGetterForCell, value = 123, script = "script")
        return cell, cellAddr

    def test_hasCellAt(self):
        s = WorksheetImp(translatorGetter = self.transGetter)
        self.assertFalse(s.hasCellAt(CellIndex(1, 1)))
        s.addCell(DataCell(CellIndex(1, 1), translatorGetter = self.transGetterForCell,value=123, script = "script"))
        self.assertTrue(s.hasCellAt(CellIndex(1, 1)))

    def test_getCell(self):
        s = WorksheetImp(translatorGetter = self.transGetter)
        cellAddr = CellIndex(12, 12)
        cell = DataCell(cellAddr,self.transGetterForCell)
        s.addCell(cell)
        self.assertEqual(cell, s.getOrMakeCell(cellAddr))

    def test_isEmpty(self):
        sheet = WorksheetImp(translatorGetter = self.transGetter)
        self.assertTrue(sheet.isEmpty())
        cell, cellAddr = self.makeTestObj()
        sheet.addCell(cell)
        self.assertFalse(sheet.isEmpty())
        sheet.removeCell(cellAddr)
        self.assertTrue(sheet.isEmpty())

    def test_containAddress(self):
        s = WorksheetImp(translatorGetter = self.transGetter)
        cell, cellAddr = self.makeTestObj()
        self.assertTrue(s.containsAddress(cellAddr))
        s.addCell(cell)
        self.assertTrue(s.containsAddress(cellAddr))
        s.removeCell(cellAddr)
        self.assertTrue(s.containsAddress(cellAddr))

    def test_cells(self):
        cell1, cellAddr1 = self.makeTestObj()
        cell2, cellAddr2 = self.makeTestObj()
        s = WorksheetImp(translatorGetter = self.transGetter)
        s.addCell(cell1)
        s.addCell(cell2)
        self.assertEqual([cell1, cell2], s.cells)
        s.removeCell(cellAddr1)
        self.assertEqual([cell2], s.cells)

    def test_getNonExistenceCell(self):
        s = WorksheetImp(translatorGetter = self.transGetter)
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
        return WorksheetImp(translatorGetter = self.transGetter)
