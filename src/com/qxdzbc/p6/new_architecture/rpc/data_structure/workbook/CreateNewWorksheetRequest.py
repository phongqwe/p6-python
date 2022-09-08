from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.WorkbookProtos_pb2 import CreateNewWorksheetRequestProto


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
