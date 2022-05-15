from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.proto.WorkbookProtos_pb2 import SaveWorkbookResponseProto


class SaveWorkbookResponse(ToProto[SaveWorkbookResponseProto]):

    def __init__(self,path: str,workbookKey: WorkbookKey|None=None, isError: bool=False, errorReport: ErrorReport|None=None):
        self.path = path
        self.workbookKey = workbookKey
        self.errorReport = errorReport
        self.isError = isError

    def toProtoObj(self) -> SaveWorkbookResponseProto:
        proto = SaveWorkbookResponseProto(
            path = self.path,
            isError = self.isError,
        )

        if self.workbookKey is not None:
            proto.workbookKey.CopyFrom(self.workbookKey.toProtoObj())

        if self.errorReport is not None:
            proto.errorReport.CopyFrom(self.errorReport.toProtoObj())


        return proto
