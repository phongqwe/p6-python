from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.proto.WorksheetProtos_pb2 import RenameWorksheetResponseProto


class RenameWorksheetResponseData(ToProto[RenameWorksheetResponseProto]):
    def __init__(self, workbookKey: WorkbookKey, oldName:str, newName:str, index:int=-1, isError:bool = False, errorReport:ErrorReport|None = None):
        self.workbookKey = workbookKey
        self.oldName = oldName
        self.index = index
        self.newName = newName
        self.isError = isError
        self.errorReport = errorReport

    def toProtoObj(self) -> RenameWorksheetResponseProto:
        rt = RenameWorksheetResponseProto()
        rt.oldName = self.oldName
        rt.newName = self.newName
        rt.index = self.index
        rt.isError = self.isError
        rt.workbookKey.CopyFrom(self.workbookKey.toProtoObj())
        if self.errorReport is not None:
            rt.errorReport.CopyFrom(self.errorReport.toProtoObj())
        return rt