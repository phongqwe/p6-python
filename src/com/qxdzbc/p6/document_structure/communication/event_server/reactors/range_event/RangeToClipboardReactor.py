from com.qxdzbc.p6.document_structure.communication.event.data_structure.common.ErrorIndicator import \
    ErrorIndicator
from com.qxdzbc.p6.document_structure.communication.event.data_structure.range_event.range_to_clipboard.RangeToClipboardRequest import \
    RangeToClipboardRequest
from com.qxdzbc.p6.document_structure.communication.event.data_structure.range_event.range_to_clipboard.RangeToClipboardResponse import \
    RangeToClipboardResponse
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import RangeGetter
from com.qxdzbc.p6.document_structure.communication.reactor.BaseEventReactor import BaseEventReactor


class RangeToClipboardReactor(BaseEventReactor[bytes, RangeToClipboardResponse]):

    def __init__(self, rangeGetter: RangeGetter):
        super().__init__()
        self.rangeGetter = rangeGetter

    def react(self, data: bytes) -> RangeToClipboardResponse:
        request = RangeToClipboardRequest.fromProtoBytes(data)
        rt = RangeToClipboardResponse(
            errorIndicator = ErrorIndicator.noError(),
            rangeId = request.rangeId,
            windowId = request.windowId
        )
        getRangeRs = self.rangeGetter(request.rangeId)
        if getRangeRs.isOk():
            targetRange = getRangeRs.value.rootRange
            copyRs = targetRange.copyToClipboardAsProto()
            if copyRs.isErr():
                rt.errorIndicator = ErrorIndicator.error(copyRs.err)
        else:
            rt.errorIndicator = ErrorIndicator.error(getRangeRs.err)

        return rt