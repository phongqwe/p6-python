from abc import ABC
from typing import Generic, TypeVar

P = TypeVar("P")


class ToProto(Generic[P], ABC):

    def toProtoBytes(self):
        """convert to a proto byte array that can be read directly by proto classes"""
        strByte = self.toProtoObj().SerializeToString()
        return strByte

    def toProtoObj(self) -> P:
        raise NotImplementedError()
