from dataclasses import dataclass
from typing import Optional

from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.proto.service.workbook.SetActiveWorksheetRequestProto_pb2 import SetActiveWorksheetRequestProto


@dataclass
class SetActiveWorksheetRequest(ToProto[SetActiveWorksheetRequestProto]):
    wbKey: WorkbookKey
    wsName: Optional[str] = None
    index:Optional[int] = None

    def toProtoObj(self) -> SetActiveWorksheetRequestProto:
        rt = SetActiveWorksheetRequestProto(
            wbKey = self.wbKey.toProtoObj(),
            wsName = self.wsName,
            index = self.index,
        )
        return rt

    @staticmethod
    def fromProtoBytes(data: bytes) -> 'SetActiveWorksheetRequest':
        proto = SetActiveWorksheetRequestProto()
        proto.ParseFromString(data)
        return SetActiveWorksheetRequest.fromProto(proto)
    
    @staticmethod
    def fromProto(proto:SetActiveWorksheetRequestProto):
        wsName = None
        if proto.HasField("wsName"):
            wsName = proto.wsName
        index = None
        if proto.HasField("index"):
            index = proto.index
        return SetActiveWorksheetRequest(
            wbKey = WorkbookKeys.fromProto(proto.wbKey),
            wsName = wsName,
            index = index
        )