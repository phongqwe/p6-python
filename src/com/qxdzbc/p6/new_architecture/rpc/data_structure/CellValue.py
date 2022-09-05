from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto, P
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellValueProto

@dataclass
class CellValue(ToProto[CellValueProto]):
    str: Optional[str] = None
    num: Optional[float] = None
    vBool: Optional[bool] = None
    def toProtoObj(self) -> CellValueProto:
        return CellValueProto(
            str = self.str,
            num = self.num,
            bool = self.vBool
        )