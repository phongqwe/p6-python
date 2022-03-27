from bicp_document_structure.message.proto.WorkbookProto_pb2 import CreateNewWorksheetProto
from bicp_document_structure.util.ToProto import ToProto, P
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.workbook.key.WorkbookKey import WorkbookKey


class CreateNewWorksheetData(ToProto[CreateNewWorksheetProto]):
    def __init__(self,workbookKey:WorkbookKey, newWorksheetName:str, isError:bool = False,errorReport:ErrorReport|None = None):
        self.wk:WorkbookKey = workbookKey
        self.wsName = newWorksheetName
        self.isError = isError
        self.errorReport = errorReport

    def toProtoObj(self) -> CreateNewWorksheetProto:
        protoData = CreateNewWorksheetProto()
        protoData.newWorksheetName = self.wsName
        protoData.workbookKey.CopyFrom(self.wk.toProtoObj())
        protoData.isError = self.isError
        if self.errorReport is not None:
            protoData.errorReport.CopyFrom(self.errorReport.toProtoObj())
        return protoData