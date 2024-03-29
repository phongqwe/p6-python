from dataclasses import dataclass

from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.proto.CommonProtos_pb2 import BoolMsgProto


@dataclass
class BoolMsg(ToProto[BoolMsgProto]):
    v:bool
    
    def toProtoObj(self) -> BoolMsgProto:
        return BoolMsgProto(v = self.v)
    
    @staticmethod
    def fromProto(proto:BoolMsgProto):
        return BoolMsg(proto.v)