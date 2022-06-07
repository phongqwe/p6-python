from com.emeraldblast.p6.document_structure.communication.event.data_structure.ToEventData import ToEventData

from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.proto.WorksheetProtos_pb2 import DeleteCellResponseProto


class DeleteCellResponse(ToEventData,ToProto[DeleteCellResponseProto]):
    def __init__(self, workbookKey: WorkbookKey, worksheetName: str, cellAddress: CellAddress,
                 workbook: Workbook = None, isError: bool = False, errorReport: ErrorReport = None):
        self.newWorkbook = workbook
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

        if self.newWorkbook is not None:
            rt.newWorkbook.CopyFrom(self.newWorkbook.toProtoObj())

        if self.errorReport is not None:
            rt.errorReport.CopyFrom(self.errorReport.toProtoObj())
        return rt
