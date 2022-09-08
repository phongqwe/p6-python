from dataclasses import dataclass

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.DocProtos_pb2 import WsWbProto


@dataclass
class WsWb(ToProto[WsWbProto]):
    workbookKey:WorkbookKey
    worksheetName:str
    def toProtoObj(self) -> WsWbProto:
        proto = WsWbProto(
            workbookKey = self.workbookKey.toProtoObj(),
            worksheetName = self.worksheetName
        )
        return proto

    @staticmethod
    def fromProto(proto:WsWbProto)->'WsWb':
        return WsWb(
            workbookKey = WorkbookKeys.fromProto(proto.workbookKey),
            worksheetName = proto.worksheetName
        )

