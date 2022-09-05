from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.document_structure.util.ToProto import ToProto, P
from com.qxdzbc.p6.proto.rpc.worksheet.WorksheetServiceProtos_pb2 import GetUsedRangeResponseProto


@dataclass
class GetUsedRangeResponse(ToProto[GetUsedRangeResponseProto]):

    rangeAddress:Optional[RangeAddress] = None

    def toProtoObj(self) -> GetUsedRangeResponseProto:
        ra = None
        if self.rangeAddress:
            ra = self.rangeAddress.toProtoObj()
        return GetUsedRangeResponseProto(
            rangeAddress = ra
        )

    @staticmethod
    def fromProto(proto:GetUsedRangeResponseProto):
        if proto.HasField("rangeAddress"):
            return GetUsedRangeResponse(rangeAddress = RangeAddresses.fromProto(proto.rangeAddress))
        else:
            return GetUsedRangeResponse()