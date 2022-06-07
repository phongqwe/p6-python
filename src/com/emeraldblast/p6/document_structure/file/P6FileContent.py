from pathlib import Path

from com.emeraldblast.p6.document_structure.file.P6FileMetaInfo import P6FileMetaInfo
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.Workbooks import Workbooks
from com.emeraldblast.p6.proto.P6FileProtos_pb2 import P6FileProto, P6FileContentProto


class P6FileContent(ToProto[P6FileProto]):

    def __init__(self, meta:P6FileMetaInfo, wb:Workbook):
        self.wb = wb
        self.meta = meta

    def toProtoObj(self) -> P6FileProto:
        proto = P6FileContentProto()
        proto.meta.CopyFrom(self.meta.toProtoObj())
        proto.workbook.CopyFrom(self.wb.toProtoObj())
        return proto

    @staticmethod
    def fromProtoBytes(data:bytes,filePath: Path | None = None):
        proto = P6FileContentProto()
        proto.ParseFromString(data)
        return P6FileContent(
            meta = P6FileMetaInfo.fromProto(proto.meta),
            wb = Workbooks.fromProto(proto.workbook,filePath)
        )