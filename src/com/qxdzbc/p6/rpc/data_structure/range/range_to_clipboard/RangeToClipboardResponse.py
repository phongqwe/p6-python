from dataclasses import dataclass
from typing import Optional

from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.rpc.data_structure.common.ErrorIndicator import \
    ErrorIndicator
from com.qxdzbc.p6.rpc.data_structure.range.RangeId import RangeId
from com.qxdzbc.p6.proto.RangeProtos_pb2 import RangeToClipboardResponseProto


@dataclass
class RangeToClipboardResponse(ToProto[RangeToClipboardResponseProto]):

    def __init__(self, errorIndicator: ErrorIndicator, rangeId: RangeId, windowId: Optional[str]):
        self.windowId = windowId
        self.errorIndicator = errorIndicator
        self.rangeId = rangeId

    def __str__(self):
        return str(self.toProtoObj())

    @staticmethod
    def fromProtoBytes(data:bytes)->'RangeToClipboardResponse':
        proto = RangeToClipboardResponseProto()
        proto.ParseFromString(data)
        rt = RangeToClipboardResponse(
            errorIndicator = ErrorIndicator.fromProto(proto.errorIndicator),
            rangeId =  RangeId.fromProto(proto.rangeId),
            windowId = None
        )
        if proto.HasField("windowId"):
            rt.windowId = proto.windowId
        return rt

    def toProtoObj(self) -> RangeToClipboardResponseProto:
        proto = RangeToClipboardResponseProto(
            errorIndicator = self.errorIndicator.toProtoObj(),
            rangeId = self.rangeId.toProtoObj()
        )
        if self.windowId:
            proto.windowId = self.windowId
        return proto
