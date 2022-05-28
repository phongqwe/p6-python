from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.proto.AppEventProtos_pb2 import CloseWorkbookResponseProto


class CloseWorkbookResponse(ToProto[CloseWorkbookResponseProto]):

    def __init__(
            self,
            isError: bool,
            workbookKey: WorkbookKey,
            windowId: str | None,
            errorReport: ErrorReport | None):
        self.errorReport = errorReport
        self.windowId = windowId
        self.workbookKey = workbookKey
        self.isError = isError


    def toProtoObj(self) -> CloseWorkbookResponseProto:
        proto = CloseWorkbookResponseProto(
            isError = self.isError,
            workbookKey = self.workbookKey.toProtoObj()
        )
        if self.windowId:
            proto.windowId = self.windowId
        if self.errorReport:
            proto.errorReport.CopyFrom(self.errorReport.toProtoObj())

        return proto