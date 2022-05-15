from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.proto.WorkbookProtos_pb2 import SaveWorkbookResponseProto


class SaveWorkbookResponse(ToProto[SaveWorkbookResponseProto]):

    def __init__(self, isError: bool, errorReport: ErrorReport, workbookKey: WorkbookKey, path: str):
        self.path = path
        self.workbookKey = workbookKey
        self.errorReport = errorReport
        self.isError = isError

    def toProtoObj(self) -> SaveWorkbookResponseProto:
        return SaveWorkbookResponseProto(
            path = self.path,
            workbookKey = self.workbookKey.toProtoObj(),
            errorReport = self.errorReport.toProtoObj(),
            isError = self.isError
        )
