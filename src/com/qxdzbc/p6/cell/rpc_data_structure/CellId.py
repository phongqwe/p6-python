from dataclasses import dataclass

from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellIdProto


@dataclass
class CellId(ToProto[CellIdProto]):
    cellAddress:CellAddress
    wbKey:WorkbookKey
    wsName:str

    @staticmethod
    def fromProto(proto:CellIdProto)->'CellId':
        return CellId(
            cellAddress = CellAddresses.fromProto(proto.cellAddress),
            wbKey = WorkbookKeys.fromProto(proto.wbKey),
            wsName = proto.wsName
        )

    def toProtoObj(self) -> CellIdProto:
        return CellIdProto(
            cellAddress = self.cellAddress.toProtoObj(),
            wbKey = self.wbKey.toProtoObj(),
            wsName = self.wsName
        )


