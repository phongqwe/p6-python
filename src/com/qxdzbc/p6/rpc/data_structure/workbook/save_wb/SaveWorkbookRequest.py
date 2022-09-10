from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.rpc.data_structure.ToP6Msg import ToP6Msg
from com.qxdzbc.p6.proto.AppProtos_pb2 import SaveWorkbookRequestProto


class SaveWorkbookRequest(ToP6Msg, ToProto[SaveWorkbookRequestProto]):

    def __init__(self, wbKey:WorkbookKey, path:str):
        self.workbookKey = wbKey
        self.path = path

    @staticmethod
    def fromProtoBytes(data:bytes)->'SaveWorkbookRequest':
        proto = SaveWorkbookRequestProto()
        proto.ParseFromString(data)
        return SaveWorkbookRequest(
            wbKey = WorkbookKeys.fromProto(proto.wbKey),
            path = proto.path
        )

    def toProtoObj(self) -> SaveWorkbookRequestProto:
        proto = SaveWorkbookRequestProto(
            wbKey = self.workbookKey.toProtoObj(),
            path = self.path
        )
        return proto

