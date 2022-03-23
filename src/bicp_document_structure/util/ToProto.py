from abc import ABC
from typing import Generic, TypeVar

from bicp_document_structure.util.ProtoUtils import ProtoUtils

P = TypeVar("P")
class ToProto(Generic[P],ABC):
    def toProtoStr(self)->str:
        """convert proto obj to a string that can be stored like a normal string"""
        return ProtoUtils.toProtoStr(self.toProtoObj())
        # return str(self.toProtoBytes(),"utf-8")

    def toProtoBytes(self):
        """convert to a proto byte array that can be read directly by proto classes"""
        strByte= self.toProtoObj().SerializeToString()
        return strByte
    
    def toProtoObj(self)->P:
        raise NotImplementedError()