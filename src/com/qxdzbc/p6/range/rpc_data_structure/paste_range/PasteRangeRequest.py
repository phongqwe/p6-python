from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.rpc.data_structure.ToP6Msg import ToP6Msg
from com.qxdzbc.p6.rpc.data_structure.WsWb import WsWb
from com.qxdzbc.p6.proto.RangeProtos_pb2 import PasteRangeRequestProto


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