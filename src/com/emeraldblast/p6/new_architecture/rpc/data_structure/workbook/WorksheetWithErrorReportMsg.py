from dataclasses import dataclass
from typing import Optional

from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet
from com.emeraldblast.p6.document_structure.worksheet.Worksheets import Worksheets
from com.emeraldblast.p6.proto.rpc.workbook.WorksheetWithErrorReportMsgProto_pb2 import \
    WorksheetWithErrorReportMsgProto


@dataclass
class WorksheetWithErrorReportMsg(ToProto[WorksheetWithErrorReportMsgProto]):

    worksheet:Optional[Worksheet] = None
    errorReport:Optional[ErrorReport] = None

    def isLegal(self):
        c1 = self.worksheet is None and self.errorReport is not None
        c2 = self.worksheet is not None and self.errorReport is None
        return c1 or c2

    def isErr(self)->bool:
        return self.errorReport is not None
    
    def toProtoObj(self) -> WorksheetWithErrorReportMsgProto:
        ws = None
        if self.worksheet:
            ws = self.worksheet.toProtoObj()
        er = None
        if self.errorReport:
            er = self.errorReport.toProtoObj()
        return WorksheetWithErrorReportMsgProto(
            worksheet = ws,
            errorReport = er,
        )
    @staticmethod
    def fromProto(proto:WorksheetWithErrorReportMsgProto,wb:Workbook):
        ws = None
        if proto.HasField("worksheet"):
            ws = Worksheets.fromProto(proto.worksheet,wb)
        er = None
        if proto.HasField("errorReport"):
            er = ErrorReport.fromProto(proto.errorReport)
        return WorksheetWithErrorReportMsg(
            worksheet = ws,
            errorReport = er
        )