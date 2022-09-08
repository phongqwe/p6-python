

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.WorkbookProtos_pb2 import DeleteWorksheetResponseProto


class DeleteWorksheetResponse(ToProto[DeleteWorksheetResponseProto]):

    def __init__(
            self,
            workbookKey: WorkbookKey = None,
            targetWorksheetList:str = None,
            isError: bool = False,
            errorReport: ErrorReport = None):
        self.errorReport = errorReport
        self.isError = isError
        if targetWorksheetList is None:
            targetWorksheetList = ""
        self.targetWorksheet:str = targetWorksheetList
        self.workbookKey = workbookKey

    @staticmethod
    def fromProtoBytes(protoBytes:bytes):
        # for testing
        rt = DeleteWorksheetResponseProto()
        rt.ParseFromString(protoBytes)
        return DeleteWorksheetResponse(
            workbookKey = WorkbookKeys.fromProto(rt.workbookKey),
            targetWorksheetList = rt.targetWorksheet,
            isError = rt.isError,
            errorReport = ErrorReport.fromProto(rt.errorReport)
        )

    def toProtoObj(self) -> DeleteWorksheetResponseProto:
        rt = DeleteWorksheetResponseProto()
        rt.workbookKey.CopyFrom(self.workbookKey.toProtoObj())
        rt.targetWorksheet = self.targetWorksheet
        rt.isError = self.isError
        if self.errorReport is not None:
            rt.errorReport.CopyFrom(self.errorReport.toProtoObj())
        return rt
