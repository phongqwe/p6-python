from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from com.qxdzbc.p6.document_structure.file.P6FileMetaInfo import P6FileMetaInfo
from com.qxdzbc.p6.document_structure.script.SimpleScriptEntry import SimpleScriptEntry
from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook
from com.qxdzbc.p6.document_structure.workbook.Workbooks import Workbooks
from com.qxdzbc.p6.proto.P6FileProtos_pb2 import P6FileProto, P6FileContentProto


@dataclass
class P6FileContent(ToProto[P6FileProto]):
    meta: P6FileMetaInfo
    wb: Workbook

    def __eq__(self, o: object) -> bool:
        if isinstance(o,P6FileContent):
            c1 = self.meta == o.meta
            c3 = self.wb.isSimilar(o.wb)
            return c1 and c3
        else:
            return False

    def toProtoObj(self) -> P6FileProto:
        proto = P6FileContentProto()
        proto.meta.CopyFrom(self.meta.toProtoObj())
        proto.workbook.CopyFrom(self.wb.toProtoObj())
        return proto

    @staticmethod
    def fromProtoBytes(data: bytes, filePath: Optional[Path] = None):
        proto = P6FileContentProto()
        proto.ParseFromString(data)

        # scripts = []
        # for scriptProto in proto.scripts:
        #     scripts.append(SimpleScriptEntry.fromProto(scriptProto))

        return P6FileContent(
            meta = P6FileMetaInfo.fromProto(proto.meta),
            wb = Workbooks.fromProto(proto.workbook, filePath),
        )
