from bicp_document_structure.communication.proto.WorksheetProtoMsg_pb2 import RenameWorksheetRequestProto
from bicp_document_structure.workbook.key.WorkbookKey import WorkbookKey
from bicp_document_structure.workbook.key.WorkbookKeys import WorkbookKeys


class RenameWorksheetRequest:

    def __init__(self, workbookKey:WorkbookKey, oldName:str, newName:str):
        self.newName = newName
        self.oldName = oldName
        self.workbookKey = workbookKey

    @staticmethod
    def fromProto(proto:RenameWorksheetRequestProto)->'RenameWorksheetRequest':
        return RenameWorksheetRequest(
            newName = proto.newName,
            oldName = proto.oldName,
            workbookKey = WorkbookKeys.fromProto(proto.workbookKey)
        )