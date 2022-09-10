from dataclasses import dataclass

from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.rpc.data_structure.CellId import CellId
from com.qxdzbc.p6.rpc.data_structure.CellValue import CellValue
from com.qxdzbc.p6.proto.DocProtos_pb2 import Cell2Proto


@dataclass
class Cell2Pr(ToProto[Cell2Proto]):
    id: CellId
    value: CellValue | None = None
    formula: str | None = None

    def toProtoObj(self) -> Cell2Proto:
        vl = None
        if self.value:
            vl = self.value.toProtoObj()
        return Cell2Proto(
            id = self.id.toProtoObj(),
            value = vl,
            formula = self.formula
        )