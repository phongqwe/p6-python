from dataclasses import dataclass

from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.proto.P6FileProtos_pb2 import P6FileMetaInfoProto

@dataclass
class P6FileMetaInfo(ToProto[P6FileMetaInfoProto]):
    date:float
    # def __init__(self, date:float):
    #     self.date = date

    def toProtoObj(self)->P6FileMetaInfoProto:
        proto = P6FileMetaInfoProto()
        proto.date = self.date
        return proto

    @staticmethod
    def fromProtoBytes(data:bytes)->'P6FileMetaInfo':
        proto = P6FileMetaInfoProto()
        proto.ParseFromString(data)
        return P6FileMetaInfo.fromProto(proto)

    @staticmethod
    def fromProto(proto:P6FileMetaInfoProto)->'P6FileMetaInfo':
        return P6FileMetaInfo(
            date = proto.date
        )

