from dataclasses import dataclass

from com.qxdzbc.p6.cell.IndCell import IndCell
from com.qxdzbc.p6.proto.DocProtos_pb2 import IndWorksheetProto
from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.worksheet.rpc_data_structure.WorksheetId import WorksheetId


@dataclass
class IndWorksheet(ToProto[IndWorksheetProto]):
    id: WorksheetId
    cells: list[IndCell]

    def toProtoObj(self) -> IndWorksheetProto:
        return IndWorksheetProto(
            id = self.id.toProtoObj(),
            cells = list(map(lambda c: c.toProtoObj(), self.cells))
        )