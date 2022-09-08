from dataclasses import dataclass, field
from typing import Optional

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.document_structure.worksheet.Worksheets import Worksheets
from com.qxdzbc.p6.proto.rpc.workbook.WorkbooKServiceProtos_pb2 import GetAllWorksheetsResponseProto


@dataclass
class GetAllWorksheetsResponse(ToProto[GetAllWorksheetsResponseProto]):
    worksheets: list[Worksheet] = field(default_factory=lambda:[])
    errorReport: Optional[ErrorReport] = None

    @staticmethod
    def fromProto(proto: GetAllWorksheetsResponseProto, wb: Workbook):
        l = []
        for wsProto in proto.worksheets:
            l.append(Worksheets.fromProto(wsProto, wb))
        err = None
        if proto.HasField("errorReport"):
            err = ErrorReport.fromProto(proto.errorReport)
        return GetAllWorksheetsResponse(worksheets = l, errorReport = err)

    def toProtoObj(self) -> GetAllWorksheetsResponseProto:
        wsProtoLst = []
        for ws in self.worksheets:
            wsProtoLst.append(ws.toProtoObj())
        proto = GetAllWorksheetsResponseProto(
            worksheets = wsProtoLst,
        )
        if self.errorReport is not None:
            proto.errorReport.CopyFrom(self.errorReport.toProtoObj())
        return proto
