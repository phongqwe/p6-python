from dataclasses import dataclass

from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.proto.WorkbookProtos_pb2 import SetWbKeyRequestProto


@dataclass
class SetWbNameRequest(ToProto[SetWbKeyRequestProto]):
    wbKey:WorkbookKey
    newWbKey:WorkbookKey
    def toProtoObj(self) -> SetWbKeyRequestProto:
        return SetWbKeyRequestProto(
            wbKey = self.wbKey.toProtoObj(),
            newWbKey = self.newWbKey.toProtoObj()
        )