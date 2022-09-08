from dataclasses import dataclass

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto, P
from com.qxdzbc.p6.proto.P6MsgProtos_pb2 import P6EventProto

@dataclass
class P6Event(ToProto[P6EventProto]):
    code:str
    name: str
    def toProtoObj(self) -> P6EventProto:
        return P6EventProto(
            code = self.code,
            name = self.name
        )

