from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.proto.AppEventProtos_pb2 import LoadWorkbookResponseProto


class LoadWorkbookResponse(ToProto[LoadWorkbookResponseProto]):
    def __init__(self, isError: bool, errorReport: ErrorReport | None = None, workbook: Workbook | None = None):
        self.workbook = workbook
        self.errorReport = errorReport
        self.isError = isError

    def toProtoObj(self)->LoadWorkbookResponseProto:
        proto = LoadWorkbookResponseProto(isError = self.isError)
        if self.workbook:
            proto.workbook.CopyFrom( self.workbook.toProtoObj())
        if self.errorReport:
            proto.errorReport.CopyFrom(self.errorReport.toProtoObj())
        return proto


