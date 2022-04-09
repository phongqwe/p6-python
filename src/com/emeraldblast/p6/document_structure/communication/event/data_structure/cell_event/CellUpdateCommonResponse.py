from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.proto.CellProtos_pb2 import CellUpdateCommonResponseProto


class CellUpdateCommonResponse(ToProto[CellUpdateCommonResponseProto]):
    def __init__(self, workbookKey:WorkbookKey,newWorkbook: Workbook | None, isError: bool = False, errorReport: ErrorReport | None = None):
        self.workbookKey = workbookKey
        self.errorReport = errorReport
        self.isError = isError
        self.newWorkbook = newWorkbook

    def toProtoObj(self) -> CellUpdateCommonResponseProto:
        rt = CellUpdateCommonResponseProto()
        rt.workbookKey.CopyFrom(self.workbookKey.toProtoObj())
        rt.isError = self.isError
        if self.newWorkbook is not None:
            rt.newWorkbook.CopyFrom(self.newWorkbook.toProtoObj())
        if self.errorReport is not None:
            rt.errorReport.CopyFrom(self.errorReport.toProtoObj())
        return rt