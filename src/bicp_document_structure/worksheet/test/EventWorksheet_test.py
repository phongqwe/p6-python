import unittest
from unittest.mock import MagicMock

from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.address.CellAddresses import CellAddresses
from bicp_document_structure.cell.address.CellIndex import CellIndex
from bicp_document_structure.formula_translator.FormulaTranslators import FormulaTranslators
from bicp_document_structure.worksheet.EventWorksheet import EventWorksheet
from bicp_document_structure.worksheet.WorksheetImp import WorksheetImp


class EventWorksheet_test(unittest.TestCase):
    def test_toProtoObj(self):
        s = WorksheetImp(translatorGetter = MagicMock(), name = "oldName")
        ss = EventWorksheet(s)
        ss.cell("@A1").value=123
        ss.cell("@B3").value=333
        o = ss.toProtoObj()
        self.assertEqual("oldName",o.name)
        self.assertEqual(s.cell("@A1").toProtoObj(),o.cell[0])
        self.assertEqual(s.cell("@B3").toProtoObj(),o.cell[1])

    @staticmethod
    def transGetter(name):
        return FormulaTranslators.mock()
    def test_InvokingReactor(self):
        sheet = WorksheetImp(name = "s3", translatorGetter = self.transGetter)
        self.a = 0

        def cb( ws, cell, event):
            self.a += 1

        self.b = 0

        def re(ws, re, event):
            self.b += 1

        self.c = 0

        def wse( wse, event):
            self.c += 1

        self.col = 0

        eventSheet = EventWorksheet(sheet,
                                    onCellEvent = cb,
                                    onWorksheetEvent = wse,
                                    onRangeEvent = re,
                                    )
        expect = DataCell(CellIndex(1, 2))

        # cell
        c1 = eventSheet.cell("@A2")
        c2 = eventSheet.cell("@B2")
        self.assertEqual(expect, c1)

        c1.value = 123
        self.assertEqual(1, self.a)

        c1.value = 456
        self.assertEqual(2, self.a)

        c2.value = "abc"
        self.assertEqual(3, self.a)

        c1.script = "mmm"
        self.assertEqual(4, self.a)

        c2.setScriptAndRun(999)
        self.assertEqual(5, self.a)

        # getCell
        c3 = eventSheet.getCell(CellAddresses.addressFromLabel("@A2"))
        c3.value = "jjj"
        self.assertEqual(6, self.a)

        # cells
        oldA = self.a
        for cell in eventSheet.cells:
            cell.value = -999
        self.assertEqual(oldA + len(eventSheet.cells), self.a)

        # range
        rng = eventSheet.range("@A1:B3")
        count = 0
        oldA = self.a
        for cell in rng.cells:
            cell.value = 123
            count += 1
        self.assertTrue(oldA + count, self.a)

        rng.reRun()
        self.assertEqual(1, self.b)