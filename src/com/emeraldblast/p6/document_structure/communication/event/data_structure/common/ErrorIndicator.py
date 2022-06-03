from dataclasses import dataclass

from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.proto.CommonProtos_pb2 import ErrorIndicatorProto


@dataclass
class ErrorIndicator(ToProto[ErrorIndicatorProto]):

    def __init__(self, isError: bool, errorReport: ErrorReport | None):
        self.isError = isError
        self.errorReport = errorReport

    def toProtoObj(self) -> ErrorIndicatorProto:
        proto = ErrorIndicatorProto(
            isError = self.isError
        )
        if self.errorReport:
            proto.errorReport.CopyFrom(self.errorReport.toProtoObj())
        return proto

    @staticmethod
    def noError() -> 'ErrorIndicator':
        return ErrorIndicator(False, None)

    @staticmethod
    def error(errReport: ErrorReport):
        return ErrorIndicator(True, errorReport = errReport)
