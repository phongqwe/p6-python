from dataclasses import dataclass
from typing import Optional, Union, Any

import numpy

from com.qxdzbc.p6.util.CanCheckEmpty import CanCheckEmpty
from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellValueProto


@dataclass
class CellValue(CanCheckEmpty, ToProto[CellValueProto]):
    vStr: Optional[str] = None
    vNum: Optional[float] = None
    vBool: Optional[bool] = None

    numericTypeList = [int, float, numpy.number]
    @staticmethod
    def _isNumber(a: Optional[Any]) -> bool:
        for tp in CellValue.numericTypeList:
            if isinstance(a,tp):
                return True
        return False

    @staticmethod
    def fromAny(a: Optional[Any]):

        if a is None:
            return CellValue.empty()
        if CellValue._isNumber(a):
            return CellValue(vNum = float(a))
        elif isinstance(a, str):
            return CellValue(vStr = a)
        elif isinstance(a, bool):
            return CellValue(vBool = a)
        else:
            raise TypeError(
                f"CellValue can only hold number, string, boolean, or nothing. The provided value is of type {type(a)}")

    @staticmethod
    def fromNum(i: float):
        return CellValue(vNum = i)

    @staticmethod
    def fromStr(i: str):
        return CellValue(vStr = i)

    @staticmethod
    def fromBool(i: bool):
        return CellValue(vBool = i)

    @staticmethod
    def fromProto(proto: CellValueProto):
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

    __empty = None

    @staticmethod
    def empty():
        if CellValue.__empty is None:
            CellValue.__empty = CellValue()
        return CellValue.__empty

    def isEmpty(self) -> bool:
        return self.vStr is None and \
               self.vNum is None and \
               self.vBool is None

    @property
    def value(self) -> Union[str, float, bool, None]:
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
