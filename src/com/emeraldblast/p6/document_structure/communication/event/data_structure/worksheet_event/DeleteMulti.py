from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.emeraldblast.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.proto.WorksheetProtos_pb2 import DeleteMultiRequestProto, DeleteMultiResponseProto


class DeleteMultiRequest:
    def __init__(self,
                 rangeList: list[RangeAddress],
                 cellList: list[CellAddress],
                 workbookKey: WorkbookKey,
                 worksheetName: str):
        self.worksheetName = worksheetName
        self.cellList = cellList
        self.workbookKey = workbookKey
        self.rangeList = rangeList

    @staticmethod
    def fromProto(proto: DeleteMultiRequestProto) -> 'DeleteMultiRequest':
        ranges = []
        for r in proto.range:
            ranges.append(RangeAddresses.fromProto(r))

        cells = []
        for c in proto.cell:
            cells.append(CellAddresses.fromProto(c))

        return DeleteMultiRequest(
            rangeList = ranges,
            cellList = cells,
            workbookKey = WorkbookKeys.fromProto(proto.workbookKey),
            worksheetName = proto.worksheetName
        )

    @staticmethod
    def fromProtoBytes(protoBytes: bytes) -> 'DeleteMultiRequest':
        proto = DeleteMultiRequestProto()
        proto.ParseFromString(protoBytes)
        return DeleteMultiRequest.fromProto(proto)


class DeleteMultiResponse(ToProto[DeleteMultiResponseProto]):
    def __init__(self,
                 isError: bool,
                 errorReport: ErrorReport | None,
                 newWorkbook: Workbook | None,
                 workbookKey: WorkbookKey, ):
        self.workbookKey = workbookKey
        self.newWorkbook = newWorkbook
        self.errorReport = errorReport
        self.isError = isError

    def toProtoObj(self) -> DeleteMultiResponseProto:
        proto = DeleteMultiResponseProto()
        proto.isError = self.isError
        if self.errorReport is not None:
            proto.errorReport.CopyFrom(self.errorReport.toProtoObj())
        if self.newWorkbook is not None:
            proto.newWorkbook.CopyFrom(self.newWorkbook.toProtoObj())
        proto.workbookKey.CopyFrom(self.workbookKey.toProtoObj())
        return proto
