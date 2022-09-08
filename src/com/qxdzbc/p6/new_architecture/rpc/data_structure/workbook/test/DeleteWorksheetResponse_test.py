import unittest

from com.qxdzbc.p6.new_architecture.communication import P6EventTableImp
from com.qxdzbc.p6.new_architecture.data_structure.workbook_event import \
    DeleteWorksheetResponse
from com.qxdzbc.p6.document_structure.workbook.WorkbookErrors import WorkbookErrors
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys


class DeleteWorksheetResponse_test(unittest.TestCase):

    def test_toEventData(self):
        o = DeleteWorksheetResponse(
            workbookKey = WorkbookKeys.fromNameAndPath("WB",None),
            targetWorksheetList = "Sheet1",
            isError = False,
            errorReport = WorkbookErrors.WorksheetAlreadyExistReport("Name")
        )
        edt = o.toEventData()
        self.assertEqual(P6EventTableImp.P6EventTableImp.i().getEventForClazz(DeleteWorksheetResponse),edt.event)
        self.assertEqual(o,edt.data)

    def test_toProto(self):
        """ obj is converted correctly to a proto obj"""
        data = DeleteWorksheetResponse(
            workbookKey = WorkbookKeys.fromNameAndPath("WB",None),
            targetWorksheetList = "Sheet1",
            isError = False,
            errorReport = WorkbookErrors.WorksheetAlreadyExistReport("Name")
        )

        protoObj = data.toProtoObj()
        self.assertEqual(data.workbookKey.toProtoObj(), protoObj.workbookKey)
        self.assertEqual(data.targetWorksheet, protoObj.targetWorksheet)
        self.assertEqual(data.isError, protoObj.isError)
        self.assertEqual(data.errorReport.toProtoObj(), protoObj.errorReport)

    def test_fromProto(self):
        """ obj is converted correctly to a proto obj"""
        data = DeleteWorksheetResponse(
            workbookKey = WorkbookKeys.fromNameAndPath("WB",None),
            targetWorksheetList = "Sheet1",
            isError = False,
            errorReport = WorkbookErrors.WorksheetAlreadyExistReport("Name")
        )

        protoBytes = data.toProtoBytes()
        data2 = DeleteWorksheetResponse.fromProtoBytes(protoBytes)
        self.assertEqual(data2.workbookKey,data.workbookKey)
        self.assertEqual(data2.targetWorksheet, data.targetWorksheet)
        self.assertEqual(data2.isError,data.isError)
        self.assertTrue(data2.errorReport.isSameErr(data.errorReport))


if __name__ == '__main__':
    unittest.main()
