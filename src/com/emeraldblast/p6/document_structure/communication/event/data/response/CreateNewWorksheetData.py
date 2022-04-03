from com.emeraldblast.p6.proto.WorkbookProtos_pb2 import CreateNewWorksheetResponseProto
from com.emeraldblast.p6.proto.WorksheetProtos_pb2 import RenameWorksheetResponseProto
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey


class CreateNewWorksheetResponseData(ToProto[CreateNewWorksheetResponseProto]):
    def __init__(self,workbookKey:WorkbookKey, newWorksheetName:str, isError:bool = False,errorReport:ErrorReport|None = None):
        self.workbookKey:WorkbookKey = workbookKey
        self.newWorksheetName = newWorksheetName
        self.isError = isError
        self.errorReport = errorReport

    def toProtoObj(self) -> RenameWorksheetResponseProto:
        protoData = CreateNewWorksheetResponseProto()
        protoData.newWorksheetName = self.newWorksheetName
        protoData.workbookKey.CopyFrom(self.workbookKey.toProtoObj())
        protoData.isError = self.isError
        if self.errorReport is not None:
            protoData.errorReport.CopyFrom(self.errorReport.toProtoObj())
        return protoData