from dataclasses import dataclass
from pathlib import Path

from com.emeraldblast.p6.document_structure.file.P6FileMetaInfo import P6FileMetaInfo
from com.emeraldblast.p6.document_structure.file.ScriptInFile import ScriptInFile
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.Workbooks import Workbooks
from com.emeraldblast.p6.proto.P6FileProtos_pb2 import P6FileProto, P6FileContentProto


@dataclass
class P6FileContent(ToProto[P6FileProto]):
    meta: P6FileMetaInfo
    wb: Workbook
    scripts: list[ScriptInFile] | None = None

    def __post_init__(self):
        if self.scripts is None:
            self.scripts = []

    def __eq__(self, o: object) -> bool:
        if isinstance(o,P6FileContent):
            c1 = self.meta == o.meta
            c2 = self.scripts == o.scripts
            c3 = self.wb.isSimilar(o.wb)
            return c1 and c2 and c3
        else:
            return False

    # def __init__(self, meta:P6FileMetaInfo, wb:Workbook, scripts:list[ScriptInFile] = None):
    #     self.wb = wb
    #     self.meta = meta
    #     if scripts is None:
    #         scripts = []
    #     self.scripts = scripts

    def toProtoObj(self) -> P6FileProto:
        proto = P6FileContentProto()
        proto.meta.CopyFrom(self.meta.toProtoObj())
        proto.workbook.CopyFrom(self.wb.toProtoObj())
        for script in self.scripts:
            proto.scripts.append(script.toProtoObj())
        return proto

    @staticmethod
    def fromProtoBytes(data: bytes, filePath: Path | None = None):
        proto = P6FileContentProto()
        proto.ParseFromString(data)

        scripts = []
        for scriptProto in proto.scripts:
            scripts.append(ScriptInFile.fromProto(scriptProto))

        return P6FileContent(
            meta = P6FileMetaInfo.fromProto(proto.meta),
            wb = Workbooks.fromProto(proto.workbook, filePath),
            scripts = scripts
        )
