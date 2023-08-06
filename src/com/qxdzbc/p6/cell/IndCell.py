from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.cell.CellContent import CellContent
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.proto.DocProtos_pb2 import IndCellProto
from com.qxdzbc.p6.cell.rpc_data_structure.CellValue import CellValue
from com.qxdzbc.p6.util.ToProto import ToProto


@dataclass
class IndCell(ToProto[IndCellProto]):
    address: CellAddress
    content: ToProto[CellContent]

    def toProtoObj(self) -> IndCellProto:
        return IndCellProto(
            address = self.address.toProtoObj(),
            content = self.content.toProtoObj()
        )

    # address:CellAddress
    # value:Optional[CellValue] = None
    # formula:Optional[str] = None
    #
    # def toProtoObj(self) -> IndCellProto:
    #     v = None
    #     if self.value:
    #         v = self.value.toProtoObj()
    #
    #     return IndCellProto(
    #         address = self.address.toProtoObj(),
    #         value = v,
    #         formula = self.formula
    #     )