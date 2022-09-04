from typing import Optional

from com.qxdzbc.p6.document_structure.communication.event.data_structure.ToEventData import ToEventData

from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.proto.WorkbookProtos_pb2 import CreateNewWorksheetResponseProto
from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import RenameWorksheetResponseProto


class CreateNewWorksheetResponse(ToEventData, ToProto[CreateNewWorksheetResponseProto]):
    def __init__(
            self,
            workbookKey: WorkbookKey,
            newWorksheetName: str,
            isError: bool = False,
            errorReport: Optional[ErrorReport] = None):
        self.workbookKey: WorkbookKey = workbookKey
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
