from dataclasses import dataclass
from typing import Optional

from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet
from com.emeraldblast.p6.document_structure.worksheet.Worksheets import Worksheets
from com.emeraldblast.p6.proto.rpc.workbook.GetWorksheetResponseProto_pb2 import \
    GetWorksheetResponseProto

@dataclass
class GetActiveWorksheetResponse(ToProto[GetWorksheetResponseProto]):
    worksheet: Optional[Worksheet] = None

    @staticmethod
    def fromProto(proto:GetWorksheetResponseProto,workbook:Workbook):
        ws = None
        if proto.HasField("worksheet"):
            ws = Worksheets.fromProto(proto.worksheet,workbook)
        return GetActiveWorksheetResponse(
            worksheet = ws
        )

    def toProtoObj(self) -> GetWorksheetResponseProto:
        ws = self.worksheet
        wsProto = None
        if ws is not None:
            wsProto = ws.toProtoObj()
        return GetWorksheetResponseProto(
            worksheet = wsProto
        )
    