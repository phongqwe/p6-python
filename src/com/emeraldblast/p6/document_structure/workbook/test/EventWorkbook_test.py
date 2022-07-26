import unittest
from pathlib import Path
from unittest.mock import MagicMock

from com.emeraldblast.p6.document_structure.communication.event.data_structure.common.ErrorIndicator import \
    ErrorIndicator
from com.emeraldblast.p6.document_structure.script.ScriptContainerErrors import ScriptContainerErrors

from com.emeraldblast.p6.document_structure.script.ScriptEntry import ScriptEntry

from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.SetActiveWorksheetResponse import \
    SetActiveWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.script_event.new_script.NewScriptNotification import \
    NewScriptNotification
from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.DeleteWorksheetResponse import \
    DeleteWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.notifier.eventData.EventData import EventData
from com.emeraldblast.p6.document_structure.formula_translator.FormulaTranslators import FormulaTranslators
from com.emeraldblast.p6.document_structure.script.ScriptEntryKey import ScriptEntryKey
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.workbook.EventWorkbook import EventWorkbook
from com.emeraldblast.p6.document_structure.workbook.WorkbookErrors import WorkbookErrors
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp


class EventWorkbook_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.s1, self.s2, self.s3, self.wb = self.makeTestObj()
        self.eventData = None
        self.x = 0

    def setActiveWorksheet_callback_fail(self, workFunction, moreTest):
        def onEvent(eventData: EventData):
            self.eventData = eventData
            self.x = 1

        eventWb = EventWorkbook(
            innerWorkbook = self.wb,
            onOtherEvent = onEvent
        )
        workFunction(eventWb)

        self.assertIsNotNone(self.eventData)
        self.assertEqual(1, self.x)
        self.assertEqual(P6Events.App.SetActiveWorksheet.event, self.eventData.event)
        dataObj: SetActiveWorksheetResponse = self.eventData.data
        self.assertEqual(True, dataObj.isError)
        self.assertIsNotNone(dataObj.errorReport)
        self.assertEqual(eventWb.workbookKey, dataObj.workbookKey)
        moreTest(dataObj)


    def test_addScriptRs_callback_run_fail(self):
        def ose(eventData: EventData):
            self.assertEqual(NewScriptNotification(
                scriptEntries=[],
                errorIndicator = ErrorIndicator.error(
                    ScriptContainerErrors.ScriptAlreadyExist.report("s1")
                )
            ), eventData.data)

        eventWb = EventWorkbook(
            innerWorkbook = self.wb,
            onScriptEvent = ose,
        )
        self.wb.addScriptRs("s1","abc")
        eventWb.addScriptRs("s1", "abc")

    def test_addScriptRs_callback_run_ok(self):
        def ose(eventData: EventData):
            self.assertEqual(NewScriptNotification(
                scriptEntries=[
                    ScriptEntry(
                        key = ScriptEntryKey(
                            name = "s1",
                            workbookKey = self.wb.workbookKey
                        ),
                        script = "abc"
                    )
                ],
                errorIndicator = ErrorIndicator.noError()
            ), eventData.data)

        eventWb = EventWorkbook(
            innerWorkbook = self.wb,
            onScriptEvent = ose
        )
        eventWb.addScriptRs("s1", "abc")

    def test_setActiveWorksheet_callback_fail(self):
        def workFunction(eventWorkbook: EventWorkbook):
            eventWorkbook.setActiveWorksheetRs("Invalid name")

        def moreTest(data: SetActiveWorksheetResponse):
            self.assertEqual("Invalid name", data.worksheetName)

        self.setActiveWorksheet_callback_fail(workFunction, moreTest)

    def test_setActiveWorksheet_callback_fail_blankName(self):
        def workFunction(eventWorkbook: EventWorkbook):
            eventWorkbook.setActiveWorksheetRs("")

        def moreTest(data: SetActiveWorksheetResponse):
            self.assertEqual("", data.worksheetName)

        self.setActiveWorksheet_callback_fail(workFunction, moreTest)

    def setActiveWorksheet_callback_ok(self, workFunction, moreTest):
        def onEvent(eventData: EventData):
            self.eventData = eventData
            self.x = 1

        eventWb = EventWorkbook(
            innerWorkbook = self.wb,
            onOtherEvent = onEvent
        )
        workFunction(eventWb)

        self.assertIsNotNone(self.eventData)
        self.assertEqual(1, self.x)
        self.assertEqual(P6Events.App.SetActiveWorksheet.event, self.eventData.event)
        dataObj: SetActiveWorksheetResponse = self.eventData.data
        self.assertEqual(False, dataObj.isError)
        self.assertIsNone(dataObj.errorReport)
        self.assertEqual(eventWb.workbookKey, dataObj.workbookKey)
        moreTest(dataObj)

    def test_setActiveWorksheet_callback_ok(self):
        def workFunction(eventWorkbook: EventWorkbook):
            eventWorkbook.setActiveWorksheet(self.s1.name)

        def moreTest(data: SetActiveWorksheetResponse):
            self.assertEqual(self.s1.name, data.worksheetName)

        self.setActiveWorksheet_callback_ok(workFunction, moreTest)

    def removeWorksheet_callback_fail(self, removeWork):
        """ test that the call back was called. And the data passed to the call back is correct"""

        self.x = 0
        self.eventData: EventData | None = None

        def onWbEvent(eventData: EventData):
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
        self.errorReport: Optional[ErrorReport] = None
        self.eventData: EventData | None = None

        def onWbEvent(eventData: EventData):
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
        self.errorReport: Optional[ErrorReport] = None
        self.eventData: EventData | None = None

        def onWbEvent(eventData: EventData):
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

        def onWbEvent(eventData: EventData):
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
        self.assertFalse(o.workbookKey.HasField("path"))
        self.assertEqual(s1.toProtoObj(), o.worksheet[0])
        self.assertEqual(s2.toProtoObj(), o.worksheet[1])
        self.assertEqual(s3.toProtoObj(), o.worksheet[2])
        w1.path = Path("someFile.qwe")
        o2 = w1.toProtoObj()
        self.assertEqual(str(w1.path.absolute()), o2.workbookKey.path)
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

        def cellCallback(eventData):
            self.a += 1

        eventWb = EventWorkbook(w, onCellEvent = cellCallback)
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
