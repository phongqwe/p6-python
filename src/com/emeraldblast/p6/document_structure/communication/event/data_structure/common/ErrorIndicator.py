from dataclasses import dataclass

from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.proto.CommonProtos_pb2 import ErrorIndicatorProto


@dataclass
class ErrorIndicator(ToProto[ErrorIndicatorProto]):

    def __init__(self, isError: bool, errorReport: ErrorReport | None = None):
        self.isError = isError
        self.errorReport = errorReport

    def toProtoObj(self) -> ErrorIndicatorProto:
        proto = ErrorIndicatorProto(
            isError = self.isError
        )
        if self.errorReport:
            proto.errorReport.CopyFrom(self.errorReport.toProtoObj())
        return proto

    __noError = None
    @staticmethod
    def noError() -> 'ErrorIndicator':
        if ErrorIndicator.__noError is None:
            ErrorIndicator.__noError = ErrorIndicator(False, None)
        return ErrorIndicator.__noError

    @staticmethod
    def error(errReport: ErrorReport):
        return ErrorIndicator(True, errorReport = errReport)

    @staticmethod
    def fromProto(proto:ErrorIndicatorProto)->'ErrorIndicator':
        rt = ErrorIndicator(
            isError = proto.isError,
            errorReport = None
        )
        if proto.HasField("errorReport"):
            rt.errorReport = ErrorReport.fromProto(proto.errorReport)

        return rt