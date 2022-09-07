from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto, P
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.document_structure.worksheet.Worksheets import Worksheets
from com.qxdzbc.p6.proto.rpc.workbook.WorkbooKServiceProtos_pb2 import WorksheetWithErrorReportMsgProto


@dataclass
class WorksheetWithErrorReportMsg(ToProto[WorksheetWithErrorReportMsgProto]):

    wsName:Optional[str] = None
    errorReport:Optional[ErrorReport] = None

    def isLegal(self):
        c1 = self.wsName is None and self.errorReport is not None
        c2 = self.wsName is not None and self.errorReport is None
        return c1 or c2

    def isErr(self)->bool:
        return self.errorReport is not None
    
    def toProtoObj(self) -> WorksheetWithErrorReportMsgProto:
        ws = None
        if self.wsName:
            ws = self.wsName
        er = None
        if self.errorReport:
            er = self.errorReport.toProtoObj()
        return WorksheetWithErrorReportMsgProto(
            wsName = ws,
            errorReport = er,
        )
    @staticmethod
    def fromProto(proto:WorksheetWithErrorReportMsgProto):
        ws = None
        if proto.HasField("wsName"):
            ws = proto.wsName
        er = None
        if proto.HasField("errorReport"):
            er = ErrorReport.fromProto(proto.errorReport)
        return WorksheetWithErrorReportMsg(
            wsName = ws,
            errorReport = er
        )