from dataclasses import dataclass
from typing import Optional

from com.emeraldblast.p6.document_structure.communication.event.data_structure.common.ErrorIndicator import \
    ErrorIndicator

from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.proto.CommonProtos_pb2 import SingleSignalResponseProto


@dataclass
class SingleSignalResponse(ToProto[SingleSignalResponseProto]):
    errorReport: Optional[ErrorReport] = None

    @staticmethod
    def fromProtoBytes(data: bytes) -> 'SingleSignalResponse':
        proto = SingleSignalResponseProto()
        proto.ParseFromString(data)
        return SingleSignalResponse.fromProto(proto)

    @staticmethod
    def fromProto(proto: SingleSignalResponseProto) -> 'SingleSignalResponse':
        err = None
        if proto.HasField("errorReport"):
            err = ErrorReport.fromProto(proto.errorReport)
        rt = SingleSignalResponse(
            errorReport = err
        )
        return rt

    def toProtoObj(self) -> SingleSignalResponseProto:
        err = None
        if self.errorReport is not None:
            err = self.errorReport.toProtoObj()
        rt = SingleSignalResponseProto(
            errorReport = err
        )
        return rt
