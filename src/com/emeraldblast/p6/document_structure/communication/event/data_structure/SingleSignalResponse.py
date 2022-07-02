from dataclasses import dataclass

from com.emeraldblast.p6.document_structure.communication.event.data_structure.common.ErrorIndicator import \
    ErrorIndicator

from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.proto.CommonProtos_pb2 import SingleSignalResponseProto


@dataclass
class SingleSignalResponse(ToProto[SingleSignalResponseProto]):

    errIndicator: ErrorIndicator
    
    @staticmethod
    def fromProtoBytes(data:bytes)->'SingleSignalResponse':
        proto = SingleSignalResponseProto()
        proto.ParseFromString(data)
        return SingleSignalResponse.fromProto(proto)

    @staticmethod
    def fromProto(proto:SingleSignalResponseProto)->'SingleSignalResponse':
        rt=SingleSignalResponse(
            errIndicator = ErrorIndicator.fromProto(proto.errIndicator)
        )
        return rt
    

    def toProtoObj(self) -> SingleSignalResponseProto:
        rt=SingleSignalResponseProto(
            errIndicator = self.errIndicator.toProtoObj()
        )
        return rt