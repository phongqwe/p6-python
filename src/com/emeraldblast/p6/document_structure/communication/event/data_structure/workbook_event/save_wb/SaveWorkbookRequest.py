from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.proto.WorkbookProtos_pb2 import SaveWorkbookRequestProto


class SaveWorkbookRequest:
    def __init__(self, workbookKey:WorkbookKey, path:str):
        self.workbookKey = workbookKey
        self.path = path
    @staticmethod
    def fromProtoBytes(data:bytes)->'SaveWorkbookRequest':
        proto = SaveWorkbookRequestProto()
        proto.ParseFromString(data)
        return SaveWorkbookRequest(
            workbookKey = WorkbookKeys.fromProto(proto),
            path = proto.path
        )
