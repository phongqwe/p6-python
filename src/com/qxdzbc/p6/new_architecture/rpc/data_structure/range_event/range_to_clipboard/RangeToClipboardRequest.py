from typing import Optional

from com.qxdzbc.p6.new_architecture.rpc.data_structure.range_event.RangeId import RangeId
from com.qxdzbc.p6.proto.RangeProtos_pb2 import RangeOperationRequestProto


class RangeToClipboardRequest:
    def __init__(self, rangeId:RangeId, windowId:Optional[str]):
        self.windowId = windowId
        self.rangeId = rangeId

    @staticmethod
    def fromProtoBytes(data:bytes)->'RangeToClipboardRequest':
        proto = RangeOperationRequestProto()
        proto.ParseFromString(data)
        return RangeToClipboardRequest.fromProto(proto)

    @staticmethod
    def fromProto(proto:RangeOperationRequestProto)->'RangeToClipboardRequest':
        wd = None
        if proto.HasField("windowId"):
            wd = proto.windowId
        o= RangeToClipboardRequest(
            rangeId = RangeId.fromProto(proto.rangeId),
            windowId = wd
        )
        return o