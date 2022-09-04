
from com.qxdzbc.p6.document_structure.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import DeleteMultiRequestProto


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


