from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.document_structure.worksheet.Worksheets import Worksheets
from com.qxdzbc.p6.new_architecture.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.new_architecture.worksheet.RpcWorksheet import RpcWorksheet
from com.qxdzbc.p6.proto.rpc.workbook.WorkbooKServiceProtos_pb2 import GetWorksheetResponseProto


@dataclass
class GetWorksheetResponse(ToProto[GetWorksheetResponseProto]):
    worksheet:Optional[Worksheet] = None

    def toProtoObj(self) -> GetWorksheetResponseProto:
        ws = None
        if self.worksheet:
            ws = self.worksheet.toProtoObj()
        return GetWorksheetResponseProto(
            worksheet = ws
        )
    @staticmethod
    def fromProto(proto:GetWorksheetResponseProto):
        ws = None
        if proto.HasField("worksheet"):
            ws = Worksheets.fromProto(proto.worksheet)
        return GetWorksheetResponse(worksheet = ws)

    @staticmethod
    def fromProto2(proto: GetWorksheetResponseProto, wbk:WorkbookKey, stubProvider: RpcStubProvider):
        ws = None
        if proto.HasField("worksheet"):
            ws = RpcWorksheet(
                name = proto.worksheet.name,
                wbKey = wbk,
                stubProvider = stubProvider
            )
        return GetWorksheetResponse(worksheet = ws)