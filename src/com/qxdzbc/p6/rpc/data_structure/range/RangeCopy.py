from com.qxdzbc.p6.cell.Cell import Cell
from com.qxdzbc.p6.cell.Cells import Cells
from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.util.Util import compareList
from com.qxdzbc.p6.rpc.data_structure.range.RangeId import RangeId
from com.qxdzbc.p6.proto.RangeProtos_pb2 import RangeCopyProto


class RangeCopy(ToProto[RangeCopyProto]):

    def __init__(self, rangeId: RangeId | None, cells: list[Cell]):
        self.cells = cells
        self.rangeId = rangeId

    def __eq__(self, other):
        if isinstance(other, RangeCopy):
            sameCells = compareList(self.cells, other.cells)
            sameRangeId = self.rangeId == other.rangeId
            return sameCells and sameRangeId
        else:
            return False

    @staticmethod
    def fromProtoBytes(data: bytes) -> 'RangeCopy':
        proto = RangeCopyProto()
        proto.ParseFromString(data)
        return RangeCopy.fromProto(proto)

    @staticmethod
    def fromProto(proto: RangeCopyProto) -> 'RangeCopy':
        return RangeCopy(
            rangeId = RangeId.fromProto(proto.id),
            cells = list(map(lambda c: Cells.fromProto(c), proto.cell))
        )

    def toProtoObj(self) -> RangeCopyProto:
        proto = RangeCopyProto(
            id = self.rangeId.toProtoObj(),
            cell = list(map(lambda c: c.toProtoObj(), self.cells))
        )
        return proto
