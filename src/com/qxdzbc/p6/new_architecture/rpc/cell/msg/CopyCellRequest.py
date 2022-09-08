from dataclasses import dataclass

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.new_architecture.rpc.data_structure.CellId import CellId
from com.qxdzbc.p6.proto.rpc.cell.CellServiceProtos_pb2 import CopyCellRequestProto


@dataclass
class CopyCellRequest(ToProto[CopyCellRequestProto]):
    fromCell: CellId
    toCell: CellId

    def toProtoObj(self) -> CopyCellRequestProto:
        return CopyCellRequestProto(
            fromCell = self.fromCell.toProtoObj(),
            toCell = self.toCell.toProtoObj()
        )
