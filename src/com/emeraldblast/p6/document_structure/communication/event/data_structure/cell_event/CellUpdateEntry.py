from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses

from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellUpdateContent import \
    CellUpdateContent
from com.emeraldblast.p6.proto.CellProtos_pb2 import CellUpdateEntryProto


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
