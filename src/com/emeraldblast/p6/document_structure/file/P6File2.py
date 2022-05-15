from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.proto.P6FileProtos_pb2 import P6FileProto


class P6File2(ToProto[P6FileProto]):
    def __init__(self,version:str, content:bytes):
        self.version: str = version
        self.content:bytes = content

    def toProtoObj(self)->P6FileProto:
        proto = P6FileProto()
        proto.version = self.version
        proto.content = self.content
        return proto

    @staticmethod
    def fromProtoBytes(data:bytes)->'P6File2':
        proto = P6FileProto()
        proto.ParseFromString(data)
        return P6File2(
            version = proto.version,
            content = proto.content
        )