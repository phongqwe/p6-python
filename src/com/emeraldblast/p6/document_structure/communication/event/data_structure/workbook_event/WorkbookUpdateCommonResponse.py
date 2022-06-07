from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.proto.WorkbookProtos_pb2 import WorkbookUpdateCommonResponseProto


class WorkbookUpdateCommonResponse(ToProto[WorkbookUpdateCommonResponseProto]):
    def __init__(self,
                 isError: bool,
                 workbookKey: WorkbookKey,
                 errorReport: ErrorReport | None = None,
                 newWorkbook: Workbook | None = None,
                  ):
        self.workbookKey = workbookKey
        self.newWorkbook = newWorkbook
        self.errorReport = errorReport
        self.isError = isError

    def toProtoObj(self) -> WorkbookUpdateCommonResponseProto:
        proto = WorkbookUpdateCommonResponseProto()
        proto.isError = self.isError
        if self.errorReport is not None:
            proto.errorReport.CopyFrom(self.errorReport.toProtoObj())
        if self.newWorkbook is not None:
            proto.newWorkbook.CopyFrom(self.newWorkbook.toProtoObj())
        proto.workbookKey.CopyFrom(self.workbookKey.toProtoObj())
        return proto
