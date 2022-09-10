from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.rpc.data_structure.worksheet.WorksheetId import WorksheetId
from com.qxdzbc.p6.worksheet.RpcWorksheet import RpcWorksheet
from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import GetWorksheetResponseProto


@dataclass
class GetWorksheetResponse(ToProto[GetWorksheetResponseProto]):
    wsId:Optional[WorksheetId] = None

    def toProtoObj(self) -> GetWorksheetResponseProto:
        ws = None
        if self.wsId:
            ws = self.wsId.toProtoObj()
        return GetWorksheetResponseProto(
            wsId = ws
        )
    @staticmethod
    def fromProto(proto:GetWorksheetResponseProto):
        ws = None
        if proto.HasField("wsId"):
            ws = WorksheetId.fromProto(proto.wsId)
        return GetWorksheetResponse(wsId = ws)

    @staticmethod
    def fromProto2(proto: GetWorksheetResponseProto, wbk:WorkbookKey, stubProvider: RpcStubProvider):
        ws = None
        if proto.HasField("worksheet"):
            ws = RpcWorksheet(
                name = proto.worksheet.name,
                wbKey = wbk,
                stubProvider = stubProvider
            )
        return GetWorksheetResponse(wsId = ws)