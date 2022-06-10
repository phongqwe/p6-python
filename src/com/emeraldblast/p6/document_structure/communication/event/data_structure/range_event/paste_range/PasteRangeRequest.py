from dataclasses import dataclass

from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.communication.event.data_structure.WsWb import WsWb
from com.emeraldblast.p6.proto.RangeProtos_pb2 import PasteRangeRequestProto


@dataclass
class PasteRangeRequest:
    anchorCell: CellAddress
    wsWb: WsWb
    windowId: str | None

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
