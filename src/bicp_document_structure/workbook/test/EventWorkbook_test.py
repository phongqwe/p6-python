import unittest
from pathlib import Path
from unittest.mock import MagicMock

from bicp_document_structure.formula_translator.FormulaTranslators import FormulaTranslators
from bicp_document_structure.communication.event.P6Events import P6Events
from bicp_document_structure.communication.event.reactor.eventData.WorkbookEventData import WorkbookEventData
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.workbook.EventWorkbook import EventWorkbook
from bicp_document_structure.workbook.WorkbookErrors import WorkbookErrors
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp
from bicp_document_structure.worksheet.WorksheetImp import WorksheetImp


class EventWorkbook_test(unittest.TestCase):
    def test_rename_onWorksheet(self):
        self.x = 0
        newName = "newName"
        oldName = "oldName"
        self.eventData: WorkbookEventData[P6Events.Worksheet.Rename.Response] | None = None

        def onWbEvent(eventData: WorkbookEventData[P6Events.Worksheet.Rename.Response]):
            self.x = 1
            self.eventData = eventData

        wb = WorkbookImp(name = "wb1")
        wb.createNewWorksheetRs(oldName)
        eventWb = EventWorkbook(wb, onWorkbookEvent = onWbEvent)
        sheet = eventWb.getWorksheet(oldName)
        sheet.renameRs(newName)
        print(sheet.name)
        self.assertEqual(1, self.x)


    def test_renameWorksheet_callback_ok(self):
        self.x = 0
        newName = "newName"
        oldName = "oldName"
        self.eventData: WorkbookEventData[P6Events.Worksheet.Rename.Response] | None = None

        def onWbEvent(eventData: WorkbookEventData[P6Events.Worksheet.Rename.Response]):
            self.x = 1
            self.eventData = eventData

        mockWb = WorkbookImp(name = "wb1")
        mockWb.createNewWorksheetRs(oldName)
        sheet = mockWb.getWorksheet(oldName)
        eventWb = EventWorkbook(mockWb, onWorkbookEvent = onWbEvent)
        rs = eventWb.renameWorksheetRs(oldName, newName)
        self.assertTrue(rs.isOk())
        self.assertEqual(newName, sheet.name)


    def test_renameWorksheet_callback_fail(self):
        self.x = 0
        newName = "newName"
        oldName = "oldName"
        self.eventData: WorkbookEventData[P6Events.Worksheet.Rename.Response] | None = None

        def onWbEvent(eventData: WorkbookEventData[P6Events.Worksheet.Rename.Response]):
            self.x = 1
            self.eventData = eventData

        mockRenameFunction = MagicMock()
        mockRenameFunction.return_value = Err(ErrorReport(
            WorkbookErrors.WorksheetNotExistReport.header,
            WorkbookErrors.WorksheetNotExistReport.Data(oldName)
        ))
        mockWb = MagicMock()
        mockWb.renameWorksheetRs = mockRenameFunction

        eventWb = EventWorkbook(mockWb, onWorkbookEvent = onWbEvent)
        eventWb.renameWorksheetRs(oldName, newName)
        self.assertTrue(self.eventData.isError)
        self.assertEqual(newName, self.eventData.data.newName)
        self.assertEqual(oldName, self.eventData.data.oldName)
        self.assertIsNotNone(self.eventData.data.errorReport)
        print(self.eventData.data.errorReport.toProtoObj())

    def test_createNewWorksheet_callback_fail(self):
        self.x = 0
        self.errorReport: ErrorReport | None = None
        self.eventData: WorkbookEventData | None = None

        def onWbEvent(eventData: WorkbookEventData):
            self.eventData = eventData.data
            self.errorReport = eventData.data.errorReport
            self.x = 1

        mockFunction = MagicMock()
        mockFunction.return_value = Err(
            ErrorReport(
                header = WorkbookErrors.WorksheetAlreadyExistReport.header,
                data = WorkbookErrors.WorksheetAlreadyExistReport.Data("SheetX")))
        mockWb = MagicMock()
        mockWb.createNewWorksheetRs = mockFunction
        eventWb = EventWorkbook(
            innerWorkbook = mockWb,
            onWorkbookEvent = onWbEvent)
        eventWb.createNewWorksheetRs("SheetX")
        self.assertEqual(1, self.x)
        self.assertEqual(WorkbookErrors.WorksheetAlreadyExistReport.header, self.errorReport.header)
        self.assertEqual("SheetX", self.errorReport.data.name)
        self.assertTrue(self.eventData.isError)
        print(self.errorReport.toProtoObj())

    def test_createNewWorksheet_callback_ok(self):
        s1, s2, s3, w1, d = self.makeTestObj()
        self.x = 0

        def onWbEvent(eventData: WorkbookEventData):
            self.eventData = eventData
            self.x = 1

        eventWb = EventWorkbook(
            innerWorkbook = w1,
            onWorkbookEvent = onWbEvent
        )
        newWb = eventWb.createNewWorksheet("SheetX")
        self.assertEqual(1, self.x)
        self.assertEqual("SheetX", newWb.name)
        self.assertFalse(self.eventData.isError)

    def test_toProtoObj(self):
        s1, s2, s3, w1, d = self.makeTestObj()
        o = w1.toProtoObj()
        self.assertEqual(w1.name, o.name)
        self.assertEqual("null", o.path.WhichOneof("kind"))
        self.assertEqual(s1.toProtoObj(), o.worksheet[0])
        self.assertEqual(s2.toProtoObj(), o.worksheet[1])
        self.assertEqual(s3.toProtoObj(), o.worksheet[2])
        w1.path = Path("someFile.qwe")
        o2 = w1.toProtoObj()
        self.assertEqual(str(w1.path.absolute()), o2.path.str)
        print(str(w1.path.absolute()))

    @staticmethod
    def transGetter(name):
        return FormulaTranslators.mock()

    def makeTestObj(self):
        s1 = WorksheetImp(name = "s1", translatorGetter = self.transGetter)
        s2 = WorksheetImp(name = "s2", translatorGetter = self.transGetter)
        s3 = WorksheetImp(name = "s3", translatorGetter = self.transGetter)
        d = [s1, s2, s3]
        w1 = WorkbookImp("w1", sheetList = d)
        return s1, s2, s3, w1, d

    def test_constructor(self):
        w = WorkbookImp("w1")
        self.a = 0

        def cb(wb, ws, cell, e):
            self.a += 1

        eventWb = EventWorkbook(w, cb, onWorkbookEvent = MagicMock())
        s1 = eventWb.createNewWorksheet("s1")
        c1 = s1.cell("@A1")
        c1.value = 123
        self.assertEqual(1, self.a)

        for ws in eventWb.worksheets:
            cell = ws.cell("@B1")
            cell.value = 456

        self.assertEqual(2, self.a)

        c2 = eventWb.activeWorksheet.cell("@Z1")
        c2.value = "abc"
        self.assertEqual(3, self.a)

        c3 = eventWb.getWorksheetByIndex(0).cell("@K1")
        c3.value = "qwe"
        self.assertEqual(4, self.a)

        c4 = eventWb.getWorksheetByName("s1").cell("@h1")
        c4.value = "mmm"
        self.assertEqual(5, self.a)

        c4 = eventWb.getWorksheet(0).cell("@h1")
        c4.value = "mmm"
        self.assertEqual(6, self.a)

    def test_Rename(self):
        s1, s2, s3, w1, d = self.makeTestObj()
        self.a = 0

        def cb(data):
            self.a += 1

        ewb = EventWorkbook(w1, onWorkbookEvent = cb)
        ewb.renameWorksheet(s1.name, "newName")
        self.assertEqual(1, self.a)
