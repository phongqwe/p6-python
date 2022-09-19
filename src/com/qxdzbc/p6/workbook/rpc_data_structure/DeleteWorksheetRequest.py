from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.WorkbookProtos_pb2 import DeleteWorksheetRequestProto


class DeleteWorksheetRequest(ToProto[DeleteWorksheetRequestProto]):

    def __init__(self, workbookKey:WorkbookKey, targetWorksheetList:str):
        self.workbookKey = workbookKey
        self.targetWorksheet:str = targetWorksheetList

    @staticmethod
    def fromProtoBytes(data:bytes)->'DeleteWorksheetRequest':
        proto =DeleteWorksheetRequestProto()
        proto.ParseFromString(data)
        return DeleteWorksheetRequest.fromProto(proto)

    @staticmethod
    def fromProto(proto:DeleteWorksheetRequestProto)->'DeleteWorksheetRequest':
        return DeleteWorksheetRequest(
            workbookKey = WorkbookKeys.fromProto(proto.workbookKey),
            targetWorksheetList = proto.targetWorksheet
        )

    def toProtoObj(self) -> DeleteWorksheetRequestProto:
        rt = DeleteWorksheetRequestProto()
        rt.targetWorksheet = self.targetWorksheet
        rt.workbookKey.CopyFrom(self.workbookKey.toProtoObj())
        return rt