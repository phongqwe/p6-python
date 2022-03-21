from abc import ABC
from typing import Generic, TypeVar

P = TypeVar("P")
class ToProto(Generic[P],ABC):
    def toProtoStr(self)->str:
        return P.SerializeToString()
    
    def toProtoObj(self)->P:
        raise NotImplementedError()