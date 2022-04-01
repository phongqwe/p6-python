from bicp_document_structure.communication.proto.CellProtos_pb2 import CellUpdateCommonResponseProto
from bicp_document_structure.util.ToProto import ToProto
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.workbook.WorkBook import Workbook


class CellUpdateCommonResponse(ToProto[CellUpdateCommonResponseProto]):
    def __init__(self, newWorkbook: Workbook | None, isError: bool = False, errorReport: ErrorReport | None = None):
        self.errorReport = errorReport
        self.isError = isError
        self.newWorkbook = newWorkbook

    def toProtoObj(self) -> CellUpdateCommonResponseProto:
        rt = CellUpdateCommonResponseProto()
        rt.isError = self.isError
        if self.newWorkbook is not None:
            rt.newWorkbook.CopyFrom(self.newWorkbook.toProtoObj())
        if self.errorReport is not None:
            rt.errorReport.CopyFrom(self.errorReport.toProtoObj())
        return rt
