from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.cell.rpc_data_structure.CellUpdateContent import \
    CellUpdateContent
from com.qxdzbc.p6.proto.CellProtos_pb2 import CellUpdateEntryProto


class CellUpdateEntry:
    def __init__(self, cellAddress: CellAddress, content: CellUpdateContent):
        self.cellAddress = cellAddress
        self.content = content

    @staticmethod
    def fromProto(proto: CellUpdateEntryProto) -> 'CellUpdateEntry':
        return CellUpdateEntry(
            cellAddress = CellAddresses.fromProto(proto.cellAddress),
            content = CellUpdateContent.fromProto(proto.content)
        )

    @staticmethod
    def fromProtoBytes(data: bytes) -> 'CellUpdateEntry':
        proto = CellUpdateEntryProto()
        proto.ParseFromString(data)
        return CellUpdateEntry.fromProto(proto)
