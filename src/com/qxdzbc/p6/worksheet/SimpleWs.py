from dataclasses import dataclass

from com.qxdzbc.p6.cell.PrimitiveCellDataContainer import SimpleDataCell
from com.qxdzbc.p6.proto.DocProtos_pb2 import WorksheetProto
from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet


@dataclass
class SimpleWs(Worksheet):
    """
    this is not a real worksheet, just a data container
    """
    name:str
    wbKey:WorkbookKey
    cells: list[SimpleDataCell]

    def toProtoObj(self) -> WorksheetProto:
        return WorksheetProto(
            name = self.name,
            cell = map(lambda c:c.toProtoObj(),self.cells),
            wbKey = self.wbKey.toProtoObj()
        )