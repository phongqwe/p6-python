import unittest

from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteMultiRequest import \
    DeleteMultiRequest
from com.qxdzbc.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteMultiResponse import \
    DeleteMultiResponse
from com.qxdzbc.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.workbook.WorkbookErrors import WorkbookErrors
from com.qxdzbc.p6.document_structure.workbook.WorkbookImp import WorkbookImp
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import DeleteMultiRequestProto


class DeleteMultiRequest_test(unittest.TestCase):
    def test_fromProto(self):
        protoObj = DeleteMultiRequestProto()
        r0 = DeleteMultiRequest(
            rangeList = [
                RangeAddresses.from2Cells(CellAddresses.fromLabel("@A1"), CellAddresses.fromLabel("@B2"))
            ],
            cellList = [
                CellAddresses.fromLabel("@K2"),
                CellAddresses.fromLabel("@L23")
            ],
            worksheetName = "S1",
            workbookKey = WorkbookKeys.fromNameAndPath("book1", None)

        )
        protoObj.range.extend(map(lambda r:r.toProtoObj(),r0.rangeList))
        protoObj.cell.extend(map(lambda c:c.toProtoObj(),r0.cellList))
        protoObj.worksheetName = r0.worksheetName
        protoObj.workbookKey.CopyFrom(r0.workbookKey.toProtoObj())

        request = DeleteMultiRequest.fromProto(protoObj)
        self.assertEqual(r0.cellList, request.cellList)
        self.assertEqual(r0.rangeList,request.rangeList)
        self.assertEqual(r0.workbookKey,request.workbookKey)
        self.assertEqual(r0.worksheetName,request.worksheetName)


class DeleteMultiResponse_test(unittest.TestCase):
    def test_toProto(self):
        r = DeleteMultiResponse(
            isError = False,
            errorReport = ErrorReport(
                header=WorkbookErrors.WorksheetNotExistReport.header
            ),
            newWorkbook = WorkbookImp("book1"),
            workbookKey = WorkbookKeys.fromNameAndPath("Key1")
        )
        proto = r.toProtoObj()
        self.assertEqual(r.isError, proto.isError)
        self.assertEqual(r.errorReport.toProtoObj(),proto.errorReport)
        self.assertEqual(r.newWorkbook.toProtoObj(),proto.newWorkbook)
        self.assertEqual(r.workbookKey.toProtoObj(),proto.workbookKey)
