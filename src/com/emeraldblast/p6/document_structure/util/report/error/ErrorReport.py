from typing import Any

from com.emeraldblast.p6.document_structure.util.ToException import ToException
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.util.ToRepStr import ToRepStr
from com.emeraldblast.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.emeraldblast.p6.proto.CommonProtos_pb2 import ErrorReportProto


class ErrorReport(ToProto[ErrorReportProto]):

    def __init__(self, header: ErrorHeader, data: Any | ToProto | ToRepStr|str ="", loc: str = ""):
        self.header = header
        self.data = data
        self.loc = loc


    @staticmethod
    def fromProto(protoObj:ErrorReportProto)->'ErrorReport':
        rt= ErrorReport(
            header = ErrorHeader(
                errorCode = protoObj.errorCode,
                errorDescription = protoObj.errorMessage
            ),
            data = "from proto"
        )
        if protoObj.data is not None:
            rt.data = protoObj.data
        return rt


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

    def isSameErr(self,another):
        if isinstance(another,ErrorReport):
            return self.header == another.header
        if isinstance(another, ErrorHeader):
            return self.header == another
        return False

    def toProtoObj(self) -> ErrorReportProto:
        proto = ErrorReportProto()
        proto.errorCode = self.header.errorCode
        proto.errorMessage = self._makeRepStr()
        if self.data is not None:
            proto.data = str(self.data)
        return proto

    def __eq__(self, other):
        if isinstance(other,ErrorReport):
            c1 = self.header == other.header
            c2 = self.data == other.data
            c3 = self.loc == other.loc
            return c1 and c2
        else:
            return False