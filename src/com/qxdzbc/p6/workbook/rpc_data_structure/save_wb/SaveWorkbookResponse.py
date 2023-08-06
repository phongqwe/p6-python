from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.AppProtos_pb2 import SaveWorkbookResponseProto


@dataclass
class SaveWorkbookResponse(ToProto[SaveWorkbookResponseProto]):
    path: str
    wbKey: Optional[WorkbookKey] = None
    errorReport: Optional[ErrorReport] = None

    @staticmethod
    def fromProto(proto: SaveWorkbookResponseProto):
        err = None
        wbk = None
        if proto.HasField("wbKey"):
            wbk = WorkbookKeys.fromProto(proto.wbKey)
        if proto.HasField("errorReport"):
            err = ErrorReport.fromProto(proto.errorReport)
        return SaveWorkbookResponse(
            path = proto.path,
            wbKey = wbk,
            errorReport = err,
        )

    def toProtoObj(self) -> SaveWorkbookResponseProto:
        proto = SaveWorkbookResponseProto(
            path = self.path,
        )

        if self.wbKey is not None:
            proto.wbKey.CopyFrom(self.wbKey.toProtoObj())

        if self.errorReport is not None:
            proto.errorReport.CopyFrom(self.errorReport.toProtoObj())

        return proto
