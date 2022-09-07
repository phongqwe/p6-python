from dataclasses import dataclass
from typing import Optional, Union

from com.qxdzbc.p6.document_structure.util.CanCheckEmpty import CanCheckEmpty
from com.qxdzbc.p6.document_structure.util.ToProto import ToProto, P
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellValueProto

@dataclass
class CellValue(CanCheckEmpty,ToProto[CellValueProto]):

    vStr: Optional[str] = None
    vNum: Optional[float] = None
    vBool: Optional[bool] = None

    @staticmethod
    def fromNum(i:float):
        return CellValue(vNum = i)

    @staticmethod
    def fromStr(i: str):
        return CellValue(vStr = i)

    @staticmethod
    def fromBool(i: bool):
        return CellValue(vBool = i)

    @staticmethod
    def fromProto(proto:CellValueProto):
        s = None
        n = None
        b = None
        if proto.HasField("str"):
            s = proto.str
        if proto.HasField("num"):
            n = proto.num
        if proto.HasField("bool"):
            b = proto.bool
        return CellValue(
            vStr = s,
            vNum = n,
            vBool = b,
        )


    @staticmethod
    def empty():
        return CellValue()

    def isEmpty(self) -> bool:
        return self.vStr \
               or self.vNum \
               or self.vBool is not None

    @property
    def value(self)->Union[str, float, bool, None]:
        if self.vStr:
            return self.vStr
        if self.vNum:
            return self.vNum
        if self.vBool is not None:
            return self.vBool
        return None


    def toProtoObj(self) -> CellValueProto:
        return CellValueProto(
            str = self.vStr,
            num = self.vNum,
            bool = self.vBool
        )