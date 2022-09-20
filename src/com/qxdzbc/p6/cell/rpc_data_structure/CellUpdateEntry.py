from dataclasses import dataclass

from com.qxdzbc.p6.cell.CellContent import CellContent
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.proto.CellProtos_pb2 import CellUpdateEntryProto
from com.qxdzbc.p6.util.ToProto import ToProto


@dataclass
class CellUpdateEntry:

    cellAddress: CellAddress
    content: ToProto[CellContent]

    # @staticmethod
    # def fromProto(proto: CellUpdateEntryProto) -> 'CellUpdateEntry':
    #     return CellUpdateEntry(
    #         cellAddress = CellAddresses.fromProto(proto.cellAddress),
    #         content = CellUpdateContent.fromProto(proto.content)
    #     )

    # @staticmethod
    # def fromProtoBytes(data: bytes) -> 'CellUpdateEntry':
    #     proto = CellUpdateEntryProto()
    #     proto.ParseFromString(data)
    #     return CellUpdateEntry.fromProto(proto)
