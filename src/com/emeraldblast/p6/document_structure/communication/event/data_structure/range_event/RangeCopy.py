from dataclasses import dataclass

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.Cells import Cells
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeId import RangeId
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.proto.RangeProtos_pb2 import RangeCopyProto


@dataclass
class RangeCopy(ToProto[RangeCopyProto]):

    def __init__(self, rangeId:RangeId, cells:list[Cell]):
        self.cells = cells
        self.rangeId = rangeId

    @staticmethod
    def fromProto(proto:RangeCopyProto):
        return RangeCopy(
            rangeId = RangeId.fromProto(proto.id),
            cells = list(map(lambda c: Cells.fromProto(c),proto.cell))
        )

    def toProtoObj(self) -> RangeCopyProto:
        proto = RangeCopyProto(
            id = self.rangeId.toProtoObj(),
            cell = list(map(lambda c: c.toProtoObj(),self.cells))
        )
        return proto







