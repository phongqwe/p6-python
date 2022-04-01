from bicp_document_structure.communication.proto.WorkbookProtoMsg_pb2 import CreateNewWorksheetProto
from bicp_document_structure.util.ToProto import ToProto, P
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.workbook.key.WorkbookKey import WorkbookKey


class CreateNewWorksheetData(ToProto[CreateNewWorksheetProto]):
    def __init__(self,workbookKey:WorkbookKey, newWorksheetName:str, isError:bool = False,errorReport:ErrorReport|None = None):
        self.workbookKey:WorkbookKey = workbookKey
        self.newWorksheetName = newWorksheetName
        self.isError = isError
        self.errorReport = errorReport

    def toProtoObj(self) -> CreateNewWorksheetProto:
        protoData = CreateNewWorksheetProto()
        protoData.newWorksheetName = self.newWorksheetName
        protoData.workbookKey.CopyFrom(self.workbookKey.toProtoObj())
        protoData.isError = self.isError
        if self.errorReport is not None:
            protoData.errorReport.CopyFrom(self.errorReport.toProtoObj())
        return protoData