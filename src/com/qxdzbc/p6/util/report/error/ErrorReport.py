from typing import Any, Union

from com.qxdzbc.p6.util.ToException import ToException
from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.util.ToRepStr import ToRepStr
from com.qxdzbc.p6.util.report.error.ErrorHeader import ErrorHeader
from com.qxdzbc.p6.proto.CommonProtos_pb2 import ErrorReportProto


class ErrorReport(ToProto[ErrorReportProto]):

    def __init__(
            self,
            header: ErrorHeader,
            data: Union[Any, ToProto, ToRepStr, str, None] = None,
            exception: Exception | None = None
    ):
        self.header = header
        self.data = data
        self.exception: Exception | None = exception

    def __str__(self):
        return str(self.header)

    @staticmethod
    def fromProto(protoObj: ErrorReportProto) -> 'ErrorReport':
        rt = ErrorReport(
            header = ErrorHeader(
                errorCode = protoObj.errorCode,
                errorDescription = protoObj.errorMessage
            ),
            data = "from proto"
        )
        if protoObj.data is not None:
            rt.data = protoObj.data
        return rt

    def toException(self) -> Exception:
        if self.exception is not None:
            if isinstance(self.exception, Exception):
                return self.exception

        if isinstance(self.data, ToException):
            return self.data.toException()
        else:
            return Exception(str(self.header))

    def _makeRepStr(self) -> str:
        # if isinstance(self.data, ToRepStr):
        #     return self.data.repStr()
        # else:
        #     return str(self.header)
        exceptionMsg = None
        if self.exception is not None:
            exceptionMsg = str(self.exception)
        if exceptionMsg:
            return str(self.header) + f"\nException: {exceptionMsg}"
        else:
            return str(self.header)

    def isSameErr(self, another):
        if isinstance(another, ErrorReport):
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
        if isinstance(other, ErrorReport):
            c1 = self.header == other.header
            c2 = self.data == other.data
            c3 = self.exception == other.exception
            return c1 and c2 and c3
        else:
            return False
