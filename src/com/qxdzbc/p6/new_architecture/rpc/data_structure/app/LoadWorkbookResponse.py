from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.AppProtos_pb2 import LoadWorkbookResponseProto

@dataclass
class LoadWorkbookResponse(ToProto[LoadWorkbookResponseProto]):
    wbKey: Optional[WorkbookKey] = None
    errorReport: Optional[ErrorReport] = None

    @staticmethod
    def fromProto(proto:LoadWorkbookResponseProto):
        wbk = None
        err = None
        if proto.HasField("wbKey"):
            wbk = WorkbookKeys.fromProto(proto.wbKey)
        if proto.HasField("errorReport"):
            err = ErrorReport.fromProto(proto.errorReport)
        return LoadWorkbookResponse(
            wbKey = wbk,
            errorReport = err
        )

    def toProtoObj(self) -> LoadWorkbookResponseProto:
        proto = LoadWorkbookResponseProto()
        if self.wbKey:
            proto.wbKey.CopyFrom(self.wbKey.toProtoObj())
        if self.errorReport:
            proto.errorReport.CopyFrom(self.errorReport.toProtoObj())
        return proto