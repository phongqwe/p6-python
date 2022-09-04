from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import WorksheetIdProto


@dataclass
class WorksheetId(ToProto[WorksheetIdProto]):
    wbKey: WorkbookKey
    wsName: Optional[str] = None
    wsIndex:Optional[int] = None

    def toProtoObj(self) -> WorksheetIdProto:
        rt = WorksheetIdProto(
            wbKey = self.wbKey.toProtoObj(),
            wsName = self.wsName,
            wsIndex = self.wsIndex,
        )
        return rt

    @staticmethod
    def fromProtoBytes(data: bytes) -> 'WorksheetId':
        proto = WorksheetIdProto()
        proto.ParseFromString(data)
        return WorksheetId.fromProto(proto)
    
    @staticmethod
    def fromProto(proto:WorksheetIdProto):
        wsName = None
        if proto.HasField("wsName"):
            wsName = proto.wsName
        index = None
        if proto.HasField("wsIndex"):
            index = proto.wsIndex
        return WorksheetId(
            wbKey = WorkbookKeys.fromProto(proto.wbKey),
            wsName = wsName,
            wsIndex = index
        )