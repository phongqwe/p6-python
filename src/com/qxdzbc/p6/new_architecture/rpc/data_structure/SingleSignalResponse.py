from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Err import Err
from com.qxdzbc.p6.document_structure.util.result.Ok import Ok
from com.qxdzbc.p6.document_structure.util.result.Result import Result
from com.qxdzbc.p6.proto.CommonProtos_pb2 import SingleSignalResponseProto


@dataclass
class SingleSignalResponse(ToProto[SingleSignalResponseProto]):
    errorReport: Optional[ErrorReport] = None

    def toRs(self) -> Result[None, ErrorReport]:
        if self.errorReport:
            return Err(self.errorReport)
        else:
            return Ok(None)

    def isOk(self) -> bool:
        return self.errorReport is None

    def isError(self) -> bool:
        return self.errorReport is not None

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
