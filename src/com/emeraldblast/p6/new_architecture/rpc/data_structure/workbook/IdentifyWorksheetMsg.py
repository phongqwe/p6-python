from dataclasses import dataclass
from typing import Optional

from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.proto.rpc.workbook.WorkbooKServiceProtos_pb2 import IdentifyWorksheetMsgProto


@dataclass
class IdentifyWorksheetMsg(ToProto[IdentifyWorksheetMsgProto]):
    wbKey: WorkbookKey
    wsName: Optional[str] = None
    wsIndex:Optional[int] = None

    def toProtoObj(self) -> IdentifyWorksheetMsgProto:
        rt = IdentifyWorksheetMsgProto(
            wbKey = self.wbKey.toProtoObj(),
            wsName = self.wsName,
            wsIndex = self.wsIndex,
        )
        return rt

    @staticmethod
    def fromProtoBytes(data: bytes) -> 'IdentifyWorksheetMsg':
        proto = IdentifyWorksheetMsgProto()
        proto.ParseFromString(data)
        return IdentifyWorksheetMsg.fromProto(proto)
    
    @staticmethod
    def fromProto(proto:IdentifyWorksheetMsgProto):
        wsName = None
        if proto.HasField("wsName"):
            wsName = proto.wsName
        index = None
        if proto.HasField("wsIndex"):
            index = proto.wsIndex
        return IdentifyWorksheetMsg(
            wbKey = WorkbookKeys.fromProto(proto.wbKey),
            wsName = wsName,
            wsIndex = index
        )