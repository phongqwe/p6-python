from dataclasses import dataclass

from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.proto.DocProtos_pb2 import WorksheetProto, IndWorksheetProto
from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import LoadDataRequestProto
from com.qxdzbc.p6.util.ToProto import ToProto, P
from com.qxdzbc.p6.worksheet.LoadType import LoadType
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet


@dataclass
class LoadDataRequest(ToProto[LoadDataRequestProto]):
    loadType: LoadType
    ws:ToProto[IndWorksheetProto]
    def toProtoObj(self) -> LoadDataRequestProto:
        return LoadDataRequestProto(
            loadType = self.loadType.toProtoObj(),
            ws = self.ws.toProtoObj(),
        )