from dataclasses import dataclass
from typing import Optional

from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.communication.event.data_structure.ToP6Msg import ToP6Msg
from com.emeraldblast.p6.document_structure.communication.event.data_structure.WsWb import WsWb
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.proto.RangeProtos_pb2 import PasteRangeRequestProto


@dataclass
class PasteRangeRequest(ToP6Msg,ToProto[PasteRangeRequestProto]):
    

    anchorCell: CellAddress
    wsWb: WsWb
    windowId: Optional[str]

    @staticmethod
    def fromProtoBytes(data: bytes) -> 'PasteRangeRequest':
        proto = PasteRangeRequestProto()
        proto.ParseFromString(data)
        windowId = None
        if proto.HasField("windowId"):
            windowId = proto.windowId
        return PasteRangeRequest(
            anchorCell = CellAddresses.fromProto(proto.anchorCell),
            wsWb = WsWb.fromProto(proto.wsWb),
            windowId = windowId
        )


    def toProtoObj(self) -> PasteRangeRequestProto:
        proto = PasteRangeRequestProto(
            anchorCell = self.anchorCell.toProtoObj(),
            wsWb = self.wsWb.toProtoObj(),
            windowId = self.windowId,
        )
        return proto