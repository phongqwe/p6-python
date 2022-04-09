import unittest

from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.DeleteWorksheetResponse import \
    DeleteWorksheetResponse
from com.emeraldblast.p6.document_structure.workbook.WorkbookErrors import WorkbookErrors
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys


class DeleteWorksheetResponse_test(unittest.TestCase):
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
