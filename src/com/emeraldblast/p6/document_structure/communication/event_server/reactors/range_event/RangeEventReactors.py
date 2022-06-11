from com.emeraldblast.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WsGetter
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.range_event.PasteRangeReactor import \
    PasteRangeReactor


class RangeEventReactors:
    def __init__(self, worksheetGetter:WsGetter):
        self.wsGetter = worksheetGetter
    def pasteRangeReactor(self)->PasteRangeReactor:
        return PasteRangeReactor(
            wsGetter = self.wsGetter
        )