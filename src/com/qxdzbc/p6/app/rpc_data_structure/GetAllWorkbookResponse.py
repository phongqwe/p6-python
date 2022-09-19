from dataclasses import dataclass, field

from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.AppProtos_pb2 import GetAllWorkbookResponseProto


@dataclass
class GetAllWorkbookResponse(ToProto[GetAllWorkbookResponseProto]):
    wbKeys: list[WorkbookKey] = field(default_factory = lambda: [])
    def toProtoObj(self) -> GetAllWorkbookResponseProto:
        wbks = list(map(lambda wbk: wbk.toProtoObj(),self.wbKeys))
        return GetAllWorkbookResponseProto(
            wbKeys = wbks
        )

    @staticmethod
    def fromProto(proto:GetAllWorkbookResponseProto):
        wbks = list(map(lambda wbKeyProto:WorkbookKeys.fromProto(wbKeyProto), proto.wbKeys))
        return GetAllWorkbookResponse(
            wbKeys = wbks
        )