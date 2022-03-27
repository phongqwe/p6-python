from bicp_document_structure.message.proto.WorkbookProto_pb2 import RenameWorksheetProto

from bicp_document_structure.util.ToProto import ToProto
from bicp_document_structure.workbook.key.WorkbookKey import WorkbookKey


class RenameWorksheetOkData(ToProto[RenameWorksheetProto]):
    def __init__(self, workbookKey: WorkbookKey, oldName:str, newName:str, index:int, isError:bool = False):
        self.workbookKey = workbookKey
        self.oldName = oldName
        self.index = index
        self.newName = newName
        self.isError = isError

    def toProtoObj(self) -> RenameWorksheetProto:
        rt = RenameWorksheetProto()
        rt.oldName = self.oldName
        rt.newName = self.newName
        rt.index = self.index
        rt.workbookKey.CopyFrom(self.workbookKey.toProtoObj())
        return rt