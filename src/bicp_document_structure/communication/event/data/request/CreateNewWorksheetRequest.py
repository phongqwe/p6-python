from bicp_document_structure.communication.proto.WorkbookProtos_pb2 import CreateNewWorksheetRequestProto
from bicp_document_structure.util.ToProto import ToProto
from bicp_document_structure.workbook.key.WorkbookKey import WorkbookKey
from bicp_document_structure.workbook.key.WorkbookKeys import WorkbookKeys


class CreateNewWorksheetRequest(ToProto[CreateNewWorksheetRequestProto]):

    def __init__(self, workbookKey: WorkbookKey, newWorkSheetName: str):
        self.workbookKey = workbookKey
        self.newWorksheetName = newWorkSheetName

    @staticmethod
    def fromProto(proto: CreateNewWorksheetRequestProto):
        return CreateNewWorksheetRequest(
            workbookKey = WorkbookKeys.fromProto(proto.workbookKey),
            newWorkSheetName = proto.newWorksheetName
        )

    def toProtoObj(self) -> CreateNewWorksheetRequestProto:
        rt = CreateNewWorksheetRequestProto()
        rt.newWorksheetName = self.newWorksheetName
        rt.workbookKey.CopyFrom(self.workbookKey.toProtoObj())
        return rt
