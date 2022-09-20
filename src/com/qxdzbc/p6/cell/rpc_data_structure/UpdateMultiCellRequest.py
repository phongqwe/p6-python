from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.cell.rpc_data_structure.CellUpdateEntry import \
    CellUpdateEntry
from com.qxdzbc.p6.proto.CellProtos_pb2 import UpdateMultiCellRequestProto


class UpdateMultiCellRequest(ToProto[UpdateMultiCellRequestProto]):
    def __init__(self, workbookKey: WorkbookKey, worksheetName: str, cellUpdateList: list[CellUpdateEntry]):
        self.cellUpdateList = cellUpdateList
        self.worksheetName = worksheetName
        self.workbookKey = workbookKey

    # @staticmethod
    # def fromProtoBytes(data: bytes) -> 'CellMultiUpdateRequest':
    #     proto = CellMultiUpdateRequestProto()
    #     proto.ParseFromString(data)
    #     updates = []
    #     for u in proto.cellUpdate:
    #         updates.append(CellUpdateEntry.fromProto(u))
    #     return CellMultiUpdateRequest(
    #         workbookKey = WorkbookKeys.fromProto(proto.workbookKey),
    #         worksheetName = proto.worksheetName,
    #         cellUpdateList = updates
    #     )
