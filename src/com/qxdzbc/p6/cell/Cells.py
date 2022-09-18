from com.qxdzbc.p6.cell.Cell import Cell
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellProto
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.cell.RpcCell import RpcCell


class Cells:
    """
    Cell factory
    """
    @staticmethod
    def fromProto(proto:CellProto)->Cell:
        rt = RpcCell(
            cellAddress = CellAddresses.fromProto(proto.id.cellAddress),
            wbKey = WorkbookKeys.fromProto(proto.id.wbKey),
            wsName = proto.id.wsName,
        )
        return rt
