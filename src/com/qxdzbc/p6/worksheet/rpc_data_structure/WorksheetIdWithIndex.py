from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.proto.DocProtos_pb2 import WorksheetIdProto
from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import WorksheetIdWithIndexProto


@dataclass
class WorksheetIdWithIndex(ToProto[WorksheetIdWithIndexProto]):
    wbKey: WorkbookKey
    wsName: Optional[str] = None
    wsIndex: Optional[int] = None

    def toProtoObj(self) -> WorksheetIdProto:
        rt = WorksheetIdWithIndexProto(
            wbKey = self.wbKey.toProtoObj(),
            wsName = self.wsName,
            wsIndex = self.wsIndex,
        )
        return rt

    @staticmethod
    def fromProtoBytes(data: bytes) -> 'WorksheetIdWithIndex':
        proto = WorksheetIdWithIndexProto()
        proto.ParseFromString(data)
        return WorksheetIdWithIndex.fromProto(proto)
    
    @staticmethod
    def fromProto(proto:WorksheetIdProto):
        wsName = None
        if proto.HasField("wsName"):
            wsName = proto.wsName
        index = None
        if proto.HasField("wsIndex"):
            index = proto.wsIndex
        return WorksheetIdWithIndex(
            wbKey = WorkbookKeys.fromProto(proto.wbKey),
            wsName = wsName,
            wsIndex = index
        )