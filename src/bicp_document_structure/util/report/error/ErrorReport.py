from typing import Any

from bicp_document_structure.message.proto.Common_pb2 import ErrorReportProto
from bicp_document_structure.util.ToException import ToException
from bicp_document_structure.util.ToJson import ToJson
from bicp_document_structure.util.ToProto import ToProto
from bicp_document_structure.util.ToRepStr import ToRepStr
from bicp_document_structure.util.report.error.ErrorHeader import ErrorHeader


class ErrorReport(ToProto[ErrorReportProto]):

    def __init__(self, header: ErrorHeader, data: Any | ToProto | ToRepStr, loc: str = ""):
        self.header = header
        self.data = data
        self.loc = loc

    def toException(self)->Exception:
        if isinstance(self.data,ToException):
            return self.data.toException()
        else:
            return Exception(str(self.data))

    def _makeRepStr(self) -> str:
        if isinstance(self.data, ToRepStr):
            return self.data.repStr()
        else:
            return str(self.header)

    def toProtoObj(self) -> ErrorReportProto:
        proto = ErrorReportProto()
        proto.errorCode = self.header.errorCode
        proto.errorMessage = self._makeRepStr()
        return proto