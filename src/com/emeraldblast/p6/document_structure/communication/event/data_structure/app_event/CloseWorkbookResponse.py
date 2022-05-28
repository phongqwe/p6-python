from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.proto.AppEventProtos_pb2 import CloseWorkbookResponseProto


class CloseWorkbookResponse(ToProto[CloseWorkbookResponseProto]):

    def __init__(
            self,
            isError: bool,
            workbookKey: WorkbookKey | None,
            windowId: str | None,
            errorReport: ErrorReport | None):
        self.errorReport = errorReport
        self.windowId = windowId
        self.workbookKey = workbookKey
        self.isError = isError

    @staticmethod
    def fromRs(rs: Result[WorkbookKey, ErrorReport], windowId:str|None) -> 'CloseWorkbookResponse':
        if rs.isOk():
            wbKey = rs.value
            return CloseWorkbookResponse(isError = rs.isErr(), workbookKey = wbKey, windowId = windowId,
                                         errorReport = None)
        else:
            return CloseWorkbookResponse(isError = rs.isErr(), workbookKey = None, windowId = windowId,
                                         errorReport = rs.err)

    def toProtoObj(self) -> CloseWorkbookResponseProto:
        proto = CloseWorkbookResponseProto(
            isError = self.isError,
        )
        if self.workbookKey:
            proto.workbookKey.CopyFrom(self.workbookKey.toProtoObj())
        if self.windowId:
            proto.windowId = self.windowId
        if self.errorReport:
            proto.errorReport.CopyFrom(self.errorReport.toProtoObj())

        return proto
