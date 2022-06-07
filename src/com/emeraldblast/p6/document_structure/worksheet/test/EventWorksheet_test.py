import unittest
from unittest.mock import MagicMock

from com.emeraldblast.p6.document_structure.cell.DataCell import DataCell
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.cell.address.CellIndex import CellIndex
from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteCellResponse import \
    DeleteCellResponse
from com.emeraldblast.p6.document_structure.communication.notifier.eventData.AppEventData import EventData
from com.emeraldblast.p6.document_structure.formula_translator.FormulaTranslators import FormulaTranslators
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp
from com.emeraldblast.p6.document_structure.worksheet.EventWorksheet import EventWorksheet
from com.emeraldblast.p6.document_structure.worksheet.WorksheetImp import WorksheetImp


class EventWorksheet_test(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.wb = WorkbookImp("WB1")
        self.s1 = self.wb.createNewWorksheet("S1")

    def test_deleteCell_ok(self):
        self.eventData = None
        def onWSEvent(data):
            self.eventData = data
        es = EventWorksheet(
            innerWorksheet = self.s1,
            onWorksheetEvent = onWSEvent)
        es.deleteCellRs(CellIndex(1,1))
        self.assertIsNotNone(self.eventData)
        response:DeleteCellResponse = self.eventData.data
        self.assertEqual(self.wb.workbookKey,response.workbookKey)
        self.assertEqual(self.s1.name,response.worksheetName)
        self.assertEqual(CellIndex(1,1),response.cellAddress)
        self.assertFalse(response.isError)
        self.assertIsNone(response.errorReport)
        self.assertEqual(self.wb,response.newWorkbook)

    def test_deleteCell_fail(self):
        self.eventData = None
        def onWSEvent(data):
            self.eventData = data
        es = EventWorksheet(
            innerWorksheet = self.s1,
            onWorksheetEvent = onWSEvent)
        address= CellIndex(-11,1)
        o=es.deleteCellRs(address)
        self.assertIsNotNone(self.eventData)
        response:DeleteCellResponse = self.eventData.data
        self.assertEqual(self.wb.workbookKey,response.workbookKey)
        self.assertEqual(self.s1.name,response.worksheetName)
        self.assertEqual(address,response.cellAddress)
        self.assertTrue(response.isError)
        self.assertIsNotNone(response.errorReport)
        self.assertIsNone(response.newWorkbook)
        self.assertEqual(o.err.header,response.errorReport.header)


    def test_rename_onWorksheet(self):
        self.x = 0
        newName = "newName"
        oldName = "oldName"
        self.eventData: EventData | None = None

        def onWbEvent(eventData: EventData):
            self.x = 1
            self.eventData = eventData

        wb = WorkbookImp(name = "wb1")
        s = wb.createNewWorksheet(oldName)
        sheet = EventWorksheet(s, onWorksheetEvent = onWbEvent)
        sheet.renameRs(newName)
        print(sheet.name)
        self.assertEqual(1, self.x)

    def test_renameWorksheet_callback_ok(self):
        self.x = 0
        newName = "newName"
        oldName = "oldName"
        self.eventData: EventData | None = None

        def onWbEvent(eventData: EventData):
            self.x = 1
            self.eventData = eventData

        mockWb = WorkbookImp(name = "wb1")
        s = mockWb.createNewWorksheet(oldName)
        sheet = EventWorksheet(s, onWorksheetEvent = onWbEvent)

        rs = sheet.renameRs(newName)
        self.assertTrue(rs.isOk())
        self.assertEqual(newName, sheet.name)

    def test_toProtoObj(self):
        s = WorksheetImp(name = "oldName", workbook = MagicMock())
        wb = WorkbookImp("W")
        wb.addWorksheet(s)
        ss = EventWorksheet(s)
        ss.cell("@A1").value = 123
        ss.cell("@B3").value = 333
        o = ss.toProtoObj()
        self.assertEqual("oldName", o.name)
        self.assertEqual(s.cell("@A1").toProtoObj(), o.cell[0])
        self.assertEqual(s.cell("@B3").toProtoObj(), o.cell[1])

    @staticmethod
    def transGetter(name):
        return FormulaTranslators.mock()

    def test_InvokingReactor(self):
        sheet = WorksheetImp(name = "s3", workbook = MagicMock())
        self.a = 0

        def cb(data: EventData):
            self.a += 1

        self.b = 0

        def re(rangeEventData: EventData):
            self.b += 1

        self.c = 0

        def wse(data: EventData):
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
        c3 = eventSheet.getCell(CellAddresses.fromLabel("@A2"))
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
