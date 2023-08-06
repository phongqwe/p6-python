from dataclasses import dataclass

from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.proto.DocProtos_pb2 import RangeIdProto


@dataclass
class RangeId(ToProto[RangeIdProto]):

    rangeAddress: RangeAddress
    wbKey: WorkbookKey
    wsName: str

    def toProtoObj(self) -> RangeIdProto:
        proto = RangeIdProto(
            wbKey = self.wbKey.toProtoObj(),
            wsName = self.wsName,
            rangeAddress = self.rangeAddress.toProtoObj(),
        )
        return proto
    
    @staticmethod
    def fromProto(proto:RangeIdProto)->'RangeId':
        return RangeId(
            wbKey = WorkbookKeys.fromProto(proto.wbKey),
            wsName = proto.wsName,
            rangeAddress = RangeAddresses.fromProto(proto.rangeAddress),
        )