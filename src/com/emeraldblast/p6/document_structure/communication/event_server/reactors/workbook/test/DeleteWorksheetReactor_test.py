import unittest

from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.DeleteWorksheetRequest import \
    DeleteWorksheetRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.DeleteWorksheetResponse import \
    DeleteWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.workbook.DeleteWorksheetReactor import \
    DeleteWorksheetReactor
from com.emeraldblast.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.workbook.WorkbookErrors import WorkbookErrors
from com.emeraldblast.p6.document_structure.workbook.WorkbookImp import WorkbookImp


class DeleteWorksheetReactor_test(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.wb = WorkbookImp("Book1")
        self.s1 = self.wb.createNewWorksheet("Sheet1")
        self.s2 = self.wb.createNewWorksheet("Sheet2")
        self.s3 = self.wb.createNewWorksheet("Sheet3")
        self.rInput = DeleteWorksheetRequest(
            workbookKey = self.wb.workbookKey,
            targetWorksheetList = self.s1.name
        )

        def wbGetter(wbk):
            return Ok(self.wb)

        self.wbGetter = wbGetter

    def test_react_deleteBlankSheetName(self):
        reactor = DeleteWorksheetReactor(
            id = "id",
            wbGetter = self.wbGetter
        )
        self.rInput.targetWorksheet = ""
        rOutput = reactor.react(self.rInput.toProtoBytes())
        self.assertEqual("", rOutput.targetWorksheet)
        self.assertEqual(self.wb.workbookKey, rOutput.workbookKey)
        self.assertTrue(rOutput.isError)
        print(rOutput.errorReport.toProtoObj())
        self.assertEqual(WorkbookErrors.WorksheetNotExistReport.header,rOutput.errorReport.header)


    def test_react_deleteNonExistSheet(self):
        reactor = DeleteWorksheetReactor(
            id = "id",
            wbGetter = self.wbGetter
        )
        self.rInput.targetWorksheet = "Invalid_Sheet"
        rOutput = reactor.react(self.rInput.toProtoBytes())
        self.assertEqual("Invalid_Sheet", rOutput.targetWorksheet)
        self.assertEqual(self.wb.workbookKey, rOutput.workbookKey)
        self.assertTrue(rOutput.isError)
        print(rOutput.errorReport.toProtoObj())
        self.assertEqual(WorkbookErrors.WorksheetNotExistReport.header,rOutput.errorReport.header)


    def test_react_failToGetWb(self):
        err = ErrorReport(
            header = ErrorHeader("qwe", "123455"),
        )

        def wbGetter(wbk):
            return Err(err)

        reactor = DeleteWorksheetReactor(
            id = "id",
            wbGetter = wbGetter
        )
        rOut = reactor.react(self.rInput.toProtoBytes())

        self.assertTrue(rOut.isError)
        self.assertEqual(self.s1.name, rOut.targetWorksheet)
        self.assertEqual(self.wb.workbookKey, rOut.workbookKey)
        self.assertEqual(err, rOut.errorReport)

    def test_react_ok(self):
        reactor = DeleteWorksheetReactor(
            id = "id",
            wbGetter = self.wbGetter
        )

        rInput = DeleteWorksheetRequest(
            workbookKey = self.wb.workbookKey,
            targetWorksheetList = self.s1.name
        )

        rOutput: DeleteWorksheetResponse = reactor.react(rInput.toProtoBytes())
        self.assertFalse(rOutput.isError)
        self.assertEqual(self.s1.name, rOutput.targetWorksheet)
        self.assertEqual(self.wb.workbookKey, rOutput.workbookKey)
        self.assertIsNone(rOutput.errorReport)


if __name__ == '__main__':
    unittest.main()
