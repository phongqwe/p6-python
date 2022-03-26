from bicp_document_structure.message.proto.WorkbookProto_pb2 import CreateNewWorksheetProto, CreateNewWorksheetFailProto
from bicp_document_structure.util.ToProto import ToProto, P
from bicp_document_structure.workbook.key.WorkbookKey import WorkbookKey


class CreateNewWorksheetData(ToProto[CreateNewWorksheetProto]):
    def __init__(self,workbookKey:WorkbookKey, newWorksheetName:str, isError:bool = False):
        self.wk:WorkbookKey = workbookKey
        self.wsName = newWorksheetName
        self.isError = isError

    def toProtoObj(self) -> CreateNewWorksheetProto:
        protoData = CreateNewWorksheetProto()
        protoData.newWorksheetName = self.wsName
        protoData.workbookKey.CopyFrom(self.wk.toProtoObj())
        return protoData

class CreateNewWorksheetFailData(ToProto[CreateNewWorksheetProto]):
    def __init__(self,workbookKey:WorkbookKey, newWorksheetName:str):
        self.wk:WorkbookKey = workbookKey
        self.wsName = newWorksheetName

    def toProtoObj(self) -> CreateNewWorksheetProto:
        protoData = CreateNewWorksheetFailProto()
        protoData.newWorksheetName = self.wsName
        protoData.workbookKey.CopyFrom(self.wk.toProtoObj())
        return protoData