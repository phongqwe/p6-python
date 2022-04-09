from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.proto.WorksheetProtos_pb2 import DeleteCellResponseProto


class DeleteCellResponse(ToProto[DeleteCellResponseProto]):
    def __init__(self, workbookKey: WorkbookKey, worksheetName: str, cellAddress: CellAddress,
                 workbook: Workbook = None, isError: bool = False, errorReport: ErrorReport = None):
        self.workbook = workbook
        self.errorReport = errorReport
        self.isError = isError
        self.worksheetName = worksheetName
        self.cellAddress = cellAddress
        self.workbookKey = workbookKey

    def toProtoObj(self) -> 'DeleteCellResponse':
        rt = DeleteCellResponseProto()
        rt.worksheetName = self.worksheetName
        rt.cellAddress.CopyFrom(self.cellAddress.toProtoObj())
        rt.workbookKey.CopyFrom(self.workbookKey.toProtoObj())
        rt.isError = self.isError

        if self.workbook is not None:
            rt.newWorkbook.CopyFrom(self.workbook.toProtoObj())

        if self.errorReport is not None:
            rt.errorReport.CopyFrom(self.errorReport.toProtoObj())
        return rt

    # @staticmethod
    # def fromProtoBytes(data:bytes)->'DeleteCellResponse':
    #     proto = DeleteCellResponseProto()
    #     proto.ParseFromString(data)
    #     rt = DeleteCellResponse(
    #         workbookKey = WorkbookKeys.fromProto(proto.workbookKey),
    #         worksheetName = proto.worksheetName,
    #         cellAddress = CellAddresses.fromProto(proto.cellAddress),
    #     )
    #
    #     if proto.HasField("newWorkbook"):
    #         rt.workbook = Workbook
