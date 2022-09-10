from dataclasses import dataclass

from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import GetAllCellResponseProto


@dataclass
class GetAllCellResponse(ToProto[GetAllCellResponseProto]):
    cellAddressList: list[CellAddress]
    
    @staticmethod
    def fromProto(proto:GetAllCellResponseProto):
        cl = []
        for c in proto.cellAddressList:
            cl.append(CellAddresses.fromProto(c))
        return GetAllCellResponse(cl)

    def toProtoObj(self) -> GetAllCellResponseProto:
        cl = []
        for c in self.cellAddressList:
            cl.append(c.toProtoObj())

        return GetAllCellResponseProto(
            cellAddressList = cl
        )
