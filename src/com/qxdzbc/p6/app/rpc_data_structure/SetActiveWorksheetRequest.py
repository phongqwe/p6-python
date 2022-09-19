from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.AppProtos_pb2 import SetActiveWorksheetRequestProto


class SetActiveWorksheetRequest(ToProto[SetActiveWorksheetRequestProto]):

    def __init__(self, workbookKey: WorkbookKey, worksheetName: str):
        self.worksheetName = worksheetName
        self.workbookKey = workbookKey

    def toProtoObj(self) -> SetActiveWorksheetRequestProto:
        rt = SetActiveWorksheetRequestProto()
        rt.workbookKey.CopyFrom(self.workbookKey.toProtoObj())
        rt.worksheetName = self.worksheetName
        return rt

    @staticmethod
    def fromProtoBytes(data:bytes) -> 'SetActiveWorksheetRequest':
        proto = SetActiveWorksheetRequestProto()
        proto.ParseFromString(data)
        return SetActiveWorksheetRequest(
            workbookKey = WorkbookKeys.fromProto(proto.workbookKey),
            worksheetName = proto.worksheetName
        )

