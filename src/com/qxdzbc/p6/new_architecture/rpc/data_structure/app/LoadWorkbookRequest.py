from dataclasses import dataclass
from pathlib import Path

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto, P
from com.qxdzbc.p6.proto.AppProtos_pb2 import LoadWorkbookRequestProto


@dataclass
class LoadWorkbookRequest(ToProto[LoadWorkbookRequestProto]):
    path: str

    def toProtoObj(self) -> LoadWorkbookRequestProto:
        return LoadWorkbookRequestProto(path = self.path)

    @property
    def absolutePath(self) -> Path:
        return Path(self.path).absolute()

    @staticmethod
    def fromProtoBytes(data: bytes) -> 'LoadWorkbookRequest':
        proto = LoadWorkbookRequestProto()
        proto.ParseFromString(data)
        return LoadWorkbookRequest(proto.path)
