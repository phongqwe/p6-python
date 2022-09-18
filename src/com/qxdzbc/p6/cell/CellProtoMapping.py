from dataclasses import dataclass
from typing import Any, Optional

from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellProto
from com.qxdzbc.p6.rpc.data_structure.CellId import CellId
from com.qxdzbc.p6.rpc.data_structure.CellValue import CellValue
from com.qxdzbc.p6.util.ToProto import ToProto, P


@dataclass
class CellProtoMapping(ToProto[CellProto]):
    """
    a direct mapping to CellProto
    """
    id: CellId
    formula: Optional[str] = None
    value: Optional[Any] = None

    def toProtoObj(self) -> CellProto:
        v = None
        if self.value:
            v = CellValue.fromAny(self.value).toProtoObj()
        return CellProto(
            id=self.id.toProtoObj(),
            formula = self.formula,
            value = v,
        )





