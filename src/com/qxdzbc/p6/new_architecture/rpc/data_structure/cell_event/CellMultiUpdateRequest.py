from com.qxdzbc.p6.new_architecture.rpc.data_structure.cell_event.CellUpdateEntry import \
    CellUpdateEntry
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.CellProtos_pb2 import CellMultiUpdateRequestProto


class CellMultiUpdateRequest:
    def __init__(self, workbookKey: WorkbookKey, worksheetName: str, cellUpdateList: list[CellUpdateEntry]):
        self.cellUpdateList = cellUpdateList
        self.worksheetName = worksheetName
        self.workbookKey = workbookKey

    @staticmethod
    def fromProtoBytes(data: bytes) -> 'CellMultiUpdateRequest':
        proto = CellMultiUpdateRequestProto()
        proto.ParseFromString(data)
        updates = []
        for u in proto.cellUpdate:
            updates.append(CellUpdateEntry.fromProto(u))
        return CellMultiUpdateRequest(
            workbookKey = WorkbookKeys.fromProto(proto.workbookKey),
            worksheetName = proto.worksheetName,
            cellUpdateList = updates
        )
