from dataclasses import dataclass
from typing import Optional

from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet
from com.emeraldblast.p6.document_structure.worksheet.Worksheets import Worksheets
from com.emeraldblast.p6.proto.service.workbook.GetActiveWorksheetResponseProto_pb2 import \
    GetActiveWorksheetResponseProto

@dataclass
class GetActiveWorksheetResponse(ToProto[GetActiveWorksheetResponseProto]):
    worksheet: Optional[Worksheet] = None

    @staticmethod
    def fromProto(proto:GetActiveWorksheetResponseProto,workbook:Workbook):
        ws = None
        if proto.HasField("worksheet"):
            ws = Worksheets.fromProto(proto.worksheet,workbook)
        return GetActiveWorksheetResponse(
            worksheet = ws
        )

    def toProtoObj(self) -> GetActiveWorksheetResponseProto:
        ws = self.worksheet
        wsProto = None
        if ws is not None:
            wsProto = ws.toProtoObj()
        return GetActiveWorksheetResponseProto(
            worksheet = wsProto
        )
    