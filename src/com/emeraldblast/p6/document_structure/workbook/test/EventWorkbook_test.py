import unittest
from pathlib import Path
from unittest.mock import MagicMock

from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.DeleteWorksheetResponse import \
    DeleteWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.CellEventData import CellEventData
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.WorkbookEventData import \
    WorkbookEventData
from com.emeraldblast.p6.document_structure.formula_translator.FormulaTranslators import FormulaTranslators
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.workbook.EventWorkbook import EventWorkbook
from com.emeraldblast.p6.document_structure.workbook.WorkbookErrors import WorkbookErrors
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp


class EventWorkbook_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.s1, self.s2, self.s3, self.wb = self.makeTestObj()

    def removeWorksheet_callback_fail(self, removeWork):
        """ test that the call back was called. And the data passed to the call back is correct"""

        self.x = 0
        self.eventData: WorkbookEventData | None = None

        def onWbEvent(eventData: WorkbookEventData):
            self.eventData = eventData
            self.x = 1

        eventWb = EventWorkbook(
            innerWorkbook = self.wb,
            onWorkbookEvent = onWbEvent)

        removeWork(eventWb)
        self.assertEqual(1, self.x)

        self.assertIsNotNone(self.eventData)
        data: DeleteWorksheetResponse = self.eventData.data
        print(data.toProtoObj())

        self.assertEqual(self.wb.workbookKey, data.workbookKey)
        self.assertTrue(data.isError)
        self.assertTrue(len(data.targetWorksheet) == 0)
        self.assertIsNotNone(data.errorReport)
        self.assertEqual(WorkbookErrors.WorksheetNotExistReport.header, data.errorReport.header)

    def test_removeWorksheet_callback_fail(self):
        invalidSheet = "InvalidSheet"

        def removeWork(eventWb: EventWorkbook):
            eventWb.deleteWorksheetRs(invalidSheet)

        self.removeWorksheet_callback_fail(removeWork)

    def test_removeWorksheetByNameRs_callback_fail(self):
        invalidSheet = "InvalidSheet"

        def removeWork(eventWb: EventWorkbook):
            eventWb.deleteWorksheetByNameRs(invalidSheet)

        self.removeWorksheet_callback_fail(removeWork)

    def test_removeWorksheetByIndexRs_callback_fail(self):
        invalidSheet = 1000

        def removeWork(eventWb: EventWorkbook):
            eventWb.deleteWorksheetByIndexRs(invalidSheet)

        self.removeWorksheet_callback_fail(removeWork)

    def removeWorksheet_callback_ok(self, removeWork):
        """ test that the call back was called. And the data passed to the call back is correct"""

        self.x = 0
        self.errorReport: ErrorReport | None = None
        self.eventData: WorkbookEventData | None = None

        def onWbEvent(eventData: WorkbookEventData):
            self.eventData = eventData
            self.errorReport = eventData.data.errorReport
            self.x = 1

        eventWb = EventWorkbook(
            innerWorkbook = self.wb,
            onWorkbookEvent = onWbEvent)

        removeWork(eventWb)

        self.assertEqual(1, self.x)
        self.assertIsNone(self.errorReport)
        self.assertIsNotNone(self.eventData)
        data: DeleteWorksheetResponse = self.eventData.data
        print(data.toProtoObj())
        self.assertEqual(self.wb.workbookKey, data.workbookKey)
        self.assertFalse(data.isError)
        self.assertEqual(self.s1.name, data.targetWorksheet)

    def test_removeWorksheetByIndexRs_callback_ok(self):
        def removeWorksheet(eventWb):
            eventWb.deleteWorksheetByIndexRs(0)

        self.removeWorksheet_callback_ok(removeWorksheet)

    def test_removeWorksheetByNameRs_callback_ok(self):
        def removeWorksheet(eventWb):
            eventWb.deleteWorksheetByNameRs(self.s1.name)

        self.removeWorksheet_callback_ok(removeWorksheet)

    def test_removeWorksheet_callback_ok(self):
        def removeWorksheet(eventWb):
            eventWb.deleteWorksheet(self.s1.name)

        self.removeWorksheet_callback_ok(removeWorksheet)

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
        s1, s2, s3, w1, = self.makeTestObj()
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

    def test_toProtoObj(self):
        s1, s2, s3, w1, = self.makeTestObj()
        o = w1.toProtoObj()
        self.assertEqual(w1.name, o.workbookKey.name)
        self.assertEqual("null", o.workbookKey.path.WhichOneof("kind"))
        self.assertEqual(s1.toProtoObj(), o.worksheet[0])
        self.assertEqual(s2.toProtoObj(), o.worksheet[1])
        self.assertEqual(s3.toProtoObj(), o.worksheet[2])
        w1.path = Path("someFile.qwe")
        o2 = w1.toProtoObj()
        self.assertEqual(str(w1.path.absolute()), o2.workbookKey.path.str)
        print(str(w1.path.absolute()))

    @staticmethod
    def transGetter(name):
        return FormulaTranslators.mock()

    def makeTestObj(self):
        w1 = WorkbookImp("w1")
        s1 = w1.createNewWorksheet("s1")
        s2 = w1.createNewWorksheet("s2")
        s3 = w1.createNewWorksheet("s3")
        return s1, s2, s3, w1

    def test_constructor(self):
        w = WorkbookImp("w1")
        self.a = 0

        def cellCallback(eventData: CellEventData):
            self.a += 1

        eventWb = EventWorkbook(w, cellCallback, onWorkbookEvent = MagicMock())
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