from com.emeraldblast.p6.document_structure.communication.event.data_structure.ToP6Msg import ToP6Msg
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto, P
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.proto.WorkbookProtos_pb2 import SaveWorkbookRequestProto


class SaveWorkbookRequest(ToP6Msg, ToProto[SaveWorkbookRequestProto]):

    def __init__(self, workbookKey:WorkbookKey, path:str):
        self.workbookKey = workbookKey
        self.path = path

    @staticmethod
    def fromProtoBytes(data:bytes)->'SaveWorkbookRequest':
        proto = SaveWorkbookRequestProto()
        proto.ParseFromString(data)
        return SaveWorkbookRequest(
            workbookKey = WorkbookKeys.fromProto(proto.workbookKey),
            path = proto.path
        )

    def toProtoObj(self) -> SaveWorkbookRequestProto:
        proto = SaveWorkbookRequestProto(
            workbookKey = self.workbookKey.toProtoObj(),
            path = self.path
        )
        return proto

