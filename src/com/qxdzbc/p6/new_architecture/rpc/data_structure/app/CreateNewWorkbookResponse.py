from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.AppProtos_pb2 import CreateNewWorkbookResponseProto


@dataclass
class CreateNewWorkbookResponse(ToProto[CreateNewWorkbookResponseProto]):
    errorReport: Optional[ErrorReport] = None
    wbKey: Optional[WorkbookKey] = None
    windowId: Optional[str] = None

    def toProtoObj(self) -> CreateNewWorkbookResponseProto:
        proto = CreateNewWorkbookResponseProto()
        if self.errorReport:
            proto.errorReport.CopyFrom(self.errorReport.toProtoObj())
        if self.wbKey:
            proto.wbKey.CopyFrom(self.wbKey.toProtoObj())
        if self.windowId:
            proto.windowId = self.windowId
        return proto

    def isErr(self)->bool:
        return self.errorReport is not None

    @staticmethod
    def fromProto(proto:CreateNewWorkbookResponseProto):
        e = None
        wbk = None
        wid = None
        if proto.HasField("errorReport"):
            e = ErrorReport.fromProto(proto.errorReport)
        if proto.HasField("wbKey"):
            wbk = WorkbookKeys.fromProto(proto.wbKey)
        if proto.HasField("windowId"):
            wid = proto.windowId
        return CreateNewWorkbookResponse(
            errorReport = e,
            wbKey = wbk,
            windowId = wid,
        )