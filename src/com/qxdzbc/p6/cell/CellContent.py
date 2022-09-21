from dataclasses import dataclass
from typing import Optional, Any

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

    @staticmethod
    def fromAny(a:Any)->'CellContent':
        return CellContent(
            value = CellValue.fromAny(a)
        )
    @staticmethod
    def fromFormula(formula:str)->'CellContent':
        return CellContent(
            formula = formula
        )
    def toProtoObj(self) -> CellContentProto:
        return CellContentProto(
            cellValue = self.value.toProtoObj(),
            formula = self.formula,
        )

