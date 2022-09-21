from dataclasses import dataclass

from com.qxdzbc.p6.cell.CellContent import CellContent
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import CellUpdateEntryProto
from com.qxdzbc.p6.util.ToProto import ToProto, P


@dataclass
class CellUpdateEntry(ToProto[CellUpdateEntryProto]):

    def toProtoObj(self) -> CellUpdateEntryProto:
        return CellUpdateEntryProto(
            cellAddress = self.cellAddress.toProtoObj(),
            content = self.content.toProtoObj()
        )

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
