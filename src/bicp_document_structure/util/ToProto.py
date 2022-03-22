from abc import ABC
from typing import Generic, TypeVar

P = TypeVar("P")
class ToProto(Generic[P],ABC):
    def toProtoStr(self)->str:
        return str(self.toProtoBytes(),"utf-8")

    def toProtoBytes(self):
        strByte= self.toProtoObj().SerializeToString()
        return strByte
    
    def toProtoObj(self)->P:
        raise NotImplementedError()