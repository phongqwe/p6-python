from abc import ABC
from dataclasses import dataclass
from typing import Any, Optional

from com.qxdzbc.p6.document_structure.util import Util
from com.qxdzbc.p6.document_structure.util.ToProto import ToProto, P
from com.qxdzbc.p6.new_architecture.rpc.data_structure.CellValue import CellValue
from com.qxdzbc.p6.proto.CellProtos_pb2 import CellContentProto


@dataclass
class CellContent(ToProto[CellContentProto]):

    formula: Optional[str]
    value: CellValue

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

