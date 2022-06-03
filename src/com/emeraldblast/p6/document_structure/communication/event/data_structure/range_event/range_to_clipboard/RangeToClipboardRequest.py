from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeId import RangeId
from com.emeraldblast.p6.proto.RangeProtos_pb2 import RangeToClipboardRequestProto


class RangeToClipboardRequest:
    def __init__(self, rangeId:RangeId, windowId:str|None):
        self.windowId = windowId
        self.rangeId = rangeId

    @staticmethod
    def fromProtoBytes(data:bytes)->'RangeToClipboardRequest':
        proto = RangeToClipboardRequestProto()
        proto.ParseFromString(data)
        return RangeToClipboardRequest.fromProto(proto)

    @staticmethod
    def fromProto(proto:RangeToClipboardRequestProto)->'RangeToClipboardRequest':
        wd = None
        if proto.HasField("windowId"):
            wd = proto.windowId
        o= RangeToClipboardRequest(
            rangeId = RangeId.fromProto(proto.rangeId),
            windowId = wd
        )
        return o