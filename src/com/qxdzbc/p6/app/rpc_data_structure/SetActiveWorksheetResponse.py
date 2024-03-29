
from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.AppProtos_pb2 import SetActiveWorksheetResponseProto


class SetActiveWorksheetResponse(ToProto[SetActiveWorksheetResponseProto]):

    def __init__(self, workbookKey: WorkbookKey=None, worksheetName: str="",isError:bool=False, errorReport:ErrorReport=None):
        self.errorReport = errorReport
        self.isError = isError
        self.worksheetName = worksheetName
        self.workbookKey = workbookKey

    def toProtoObj(self) -> SetActiveWorksheetResponseProto:
        rt = SetActiveWorksheetResponseProto()
        rt.workbookKey.CopyFrom(self.workbookKey.toProtoObj())
        rt.worksheetName = self.worksheetName
        rt.isError = self.isError
        if self.errorReport is not None:
            rt.errorReport.CopyFrom(self.errorReport.toProtoObj())
        return rt

    @staticmethod
    def fromProtoBytes(data:bytes) -> 'SetActiveWorksheetResponse':
        proto = SetActiveWorksheetResponseProto()
        proto.ParseFromString(data)
        err = None
        if proto.HasField("errorReport"):
            err = ErrorReport.fromProto(proto.errorReport)
        return SetActiveWorksheetResponse(
            workbookKey = WorkbookKeys.fromProto(proto.workbookKey),
            worksheetName = proto.worksheetName,
            isError = proto.isError,
            errorReport = err
        )

