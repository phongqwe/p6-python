from pathlib import Path

from bicp_document_structure.communication.proto.DocProto_pb2 import WorkbookKeyProto
from bicp_document_structure.util.ProtoUtils import ProtoUtils
from bicp_document_structure.workbook.key.WorkbookKey import WorkbookKey
from bicp_document_structure.workbook.key.WorkbookKeyImp import WorkbookKeyImp


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