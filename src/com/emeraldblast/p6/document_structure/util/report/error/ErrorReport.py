from typing import Any

from com.emeraldblast.p6.proto.CommonProtos_pb2 import ErrorReportProto
from com.emeraldblast.p6.document_structure.util.ToException import ToException
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.util.ToRepStr import ToRepStr
from com.emeraldblast.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader


class ErrorReport(ToProto[ErrorReportProto]):

    def __init__(self, header: ErrorHeader, data: Any | ToProto | ToRepStr ="", loc: str = ""):
        self.header = header
        self.data = data
        self.loc = loc


    @staticmethod
    def fromProto(protoObj:ErrorReportProto)->'ErrorReport':
        return ErrorReport(
            header = ErrorHeader(
                errorCode = protoObj.errorCode,
                errorDescription = protoObj.errorMessage
            ),
            data = "from proto"
        )


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

    def isSameErr(self,another:'ErrorReport'):
        return self.header == another.header

    def toProtoObj(self) -> ErrorReportProto:
        proto = ErrorReportProto()
        proto.errorCode = self.header.errorCode
        proto.errorMessage = self._makeRepStr()
        return proto