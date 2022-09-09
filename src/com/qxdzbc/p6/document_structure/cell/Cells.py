from com.qxdzbc.p6.document_structure.cell.Cell import Cell
from com.qxdzbc.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.new_architecture.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.new_architecture.rpc.cell.RpcCell import RpcCell
from com.qxdzbc.p6.proto.DocProtos_pb2 import Cell2Proto, CellProto


class Cells:
    """
    Cell factory
    """
    @staticmethod
    def fromProto2(proto:Cell2Proto)->Cell:
        rt = RpcCell(
            cellAddress = CellAddresses.fromProto(proto.id.cellAddress),
            wbKey = WorkbookKeys.fromProto(proto.id.wbKey),
            wsName = proto.id.wsName,
        )
        return rt
