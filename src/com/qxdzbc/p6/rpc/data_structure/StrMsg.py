from dataclasses import dataclass

from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.proto.CommonProtos_pb2 import StrMsgProto


@dataclass
class StrMsg(ToProto[StrMsgProto]):
    v: str
    
    @staticmethod
    def fromProto(proto:StrMsgProto):
        return StrMsg(v = proto.v)
    
    def toProtoObj(self) -> StrMsgProto:
        return StrMsgProto(v = self.v)

    
    