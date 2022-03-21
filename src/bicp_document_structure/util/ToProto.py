from abc import ABC
from typing import Generic, TypeVar

P = TypeVar("P")
class ToProto(Generic[P],ABC):
    def toProtoStr(self)->str:
        strByte= self.toProtoObj().SerializeToString()
        return str(strByte,"utf-8")
    
    def toProtoObj(self)->P:
        raise NotImplementedError()