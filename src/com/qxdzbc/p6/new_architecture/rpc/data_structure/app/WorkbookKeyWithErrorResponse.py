from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.AppProtos_pb2 import WorkbookKeyWithErrorResponseProto


@dataclass
class WorkbookKeyWithErrorResponse(ToProto[WorkbookKeyWithErrorResponseProto]):
    wbKey:Optional[WorkbookKey] = None
    errorReport:Optional[ErrorReport] = None

    def isOk(self)->bool:
        return self.errorReport is None

    def isErr(self)->bool:
        return self.errorReport is not None

    def toProtoObj(self) -> WorkbookKeyWithErrorResponseProto:
        wbk = None
        err = None
        if self.wbKey:
            wbk = self.wbKey.toProtoObj()
        if self.errorReport:
            err = self.errorReport.toProtoObj()
        return WorkbookKeyWithErrorResponseProto(
            wbKey = wbk,
            errorReport = err
        )

    @staticmethod
    def fromProto(proto:WorkbookKeyWithErrorResponseProto):
        wbk = None
        err = None
        if proto.HasField("errorReport"):
            err = ErrorReport.fromProto(proto.errorReport)
        if proto.HasField("wbKey"):
            wbk = WorkbookKeys.fromProto(proto.wbKey)
        return WorkbookKeyWithErrorResponse(
            wbKey = wbk,
            errorReport = err
        )