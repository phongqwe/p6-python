from dataclasses import dataclass

from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.cell.rpc_data_structure.CellId import CellId
from com.qxdzbc.p6.proto.CellProtos_pb2 import CopyCellRequestProto


@dataclass
class CopyCellRequest(ToProto[CopyCellRequestProto]):
    fromCell: CellId
    toCell: CellId
    shiftRange:bool = True

    def toProtoObj(self) -> CopyCellRequestProto:
        return CopyCellRequestProto(
            fromCell = self.fromCell.toProtoObj(),
            toCell = self.toCell.toProtoObj(),
            shiftRange = self.shiftRange
        )
