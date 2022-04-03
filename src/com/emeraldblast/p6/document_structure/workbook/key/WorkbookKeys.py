from pathlib import Path

from com.emeraldblast.p6.proto.DocProtos_pb2 import WorkbookKeyProto
from com.emeraldblast.p6.document_structure.util.ProtoUtils import ProtoUtils
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeyImp import WorkbookKeyImp


class WorkbookKeys:
    @staticmethod
    def fromPathStr(path: str) -> WorkbookKey:
        return WorkbookKeyImp.fromPathStr(path)

    @staticmethod
    def fromNameAndPath(name: str, path: str | Path | None) -> WorkbookKey:
        p = path
        if path is not None:
            if isinstance(path, str):
                p = Path(path)
        return WorkbookKeyImp(name, p)

    @staticmethod
    def fromProto(protoOjb: WorkbookKeyProto) -> 'WorkbookKeyImp':
        p = None
        if ProtoUtils.isValidStr(protoOjb.path):
            p = Path(protoOjb.path.str)
        return WorkbookKeyImp(
            fileName = protoOjb.name,
            filePath = p
        )