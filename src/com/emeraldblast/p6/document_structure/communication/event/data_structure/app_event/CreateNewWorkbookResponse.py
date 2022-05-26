from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.proto.AppEventProtos_pb2 import CreateNewWorkbookResponseProto


class CreateNewWorkbookResponse(ToProto[CreateNewWorkbookResponseProto]):

    def __init__(
            self, isError: bool,
            errorReport: ErrorReport | None = None,
            workbook: Workbook | None = None,
            windowId: str | None = None):
        self.windowId = windowId
        self.workbook = workbook
        self.errorReport = errorReport
        self.isError = isError

    def toProtoObj(self) -> CreateNewWorkbookResponseProto:
        proto = CreateNewWorkbookResponseProto(isError = self.isError)
        if self.errorReport:
            proto.errorReport.CopyFrom(self.errorReport.toProtoObj())
        if self.workbook:
            proto.workbook.CopyFrom(self.workbook.toProtoObj())
        if self.windowId:
            proto.windowId = self.windowId
        return proto

