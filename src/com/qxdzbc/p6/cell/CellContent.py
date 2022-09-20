from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.util.CanCheckEmpty import CanCheckEmpty
from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.cell.rpc_data_structure.CellValue import CellValue
from com.qxdzbc.p6.proto.CellProtos_pb2 import CellContentProto


@dataclass
class CellContent(ToProto[CellContentProto],CanCheckEmpty):

    value: CellValue = CellValue.empty()
    formula: Optional[str] = None

    def isEmpty(self) -> bool:
        c1 = self.formula is None
        c2 = self.value.isEmpty()
        return c1 and c2

    @staticmethod
    def fromProto(proto:CellContentProto)->'CellContent':
        return CellContent(
            formula = proto.formula,
            value = CellValue.fromProto(proto.cellValue)
        )

    def toProtoObj(self) -> CellContentProto:
        cv = self.value.toProtoObj()
        return CellContentProto(
            cellValue = cv,
            formula = self.formula,
        )

