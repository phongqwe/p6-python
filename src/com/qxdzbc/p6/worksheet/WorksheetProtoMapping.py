from dataclasses import dataclass

from com.qxdzbc.p6.cell.CellProtoMapping import CellProtoMapping
from com.qxdzbc.p6.proto.DocProtos_pb2 import WorksheetProto
from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet


@dataclass
class WorksheetProtoMapping(ToProto[WorksheetProto]):
    """
    a direct mapping to WorksheetProto
    """
    name:str
    wbKey:WorkbookKey
    cells: list[CellProtoMapping]

    def toProtoObj(self) -> WorksheetProto:
        return WorksheetProto(
            name = self.name,
            cells = map(lambda c:c.toProtoObj(),self.cells),
            wbKey = self.wbKey.toProtoObj()
        )